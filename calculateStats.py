#!/usr/bin/env python3

"""
This script calculates basic statistical measures for each
trip_pair. The basic measures are: mean, median, standard deviation.
"""
import argparse
import psycopg2
import sys
import itertools
import statistics

import logging
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - %(message)s')
  
def get_existing_trip_pairs(conn, member_type, minimum):
  """get existing trip_pairs based on member_type and a minimum
  quantity of trips. The member_type values are: 
  Both, Casual, Registered"""
  
  query = """SELECT tp.start_id, tp.stop_id, tp.distance, 
          tq.quantity, tq.trip_pair_id
          FROM trip_pairs tp, trip_quantity tq 
          WHERE tp.id = tq.trip_pair_id AND tq.member_type=%s
          AND tq.quantity > %s"""
  with conn:
    with conn.cursor() as cur:
      params = (member_type, minimum)
      cur.execute(query, params)
      rows = cur.fetchall()
  return rows

def calculate_stats(member_type, minimum):
  try:
    conn = psycopg2.connect(dbname='gisdb', user='gisuser',
                            password='gis')
  except:
    print("Cannot connect to database")
    sys.exit(1)

  queryAll = """SELECT duration FROM trips 
               WHERE start_id=%s and stop_id=%s"""
  queryByType = """SELECT duration FROM trips t, member_types m
                WHERE start_id=%s and stop_id=%s AND
                t.member_type_id=m.id AND m.type IN %s"""
          
  pairList = get_existing_trip_pairs(conn, member_type, minimum)
  logging.debug(len(pairList))
  # convert the member_type to appropriate tuple for IN clause
  if member_type == 'Both':
    mType= ('Casual','Registered')
  else:
    mType = (member_type,)
  
  with conn.cursor() as qCur:
    for pair in pairList:
      (start_id, stop_id, distance, quantity, pair_id) = pair
      logging.debug((start_id, stop_id))
      params = (start_id, stop_id, mType)
      qCur.execute(queryByType, params)
      rows = qCur.fetchall()
      data = list(itertools.chain(*rows))
      # calculate the stats
      median = statistics.median(data)
      # create the execute cursor
      with conn.cursor() as eCur:
        stmt = """INSERT INTO trip_stats 
          (trip_pair_id, sample_size, conditions,
          stat_name, stat_value) VALUES (%s, %s, %s, %s, %s)"""
        eParams =  (pair_id, quantity, member_type, 'median', median)
        eCur.execute(stmt, eParams)

  conn.commit()
      
  
if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('--type', dest='member_type', default='Both', choices=['Both','Casual','Registered'], help='specify member type')
  parser.add_argument('--minimum', type=int, default=400)
  args = parser.parse_args()
  
  calculate_stats(args.member_type, args.minimum)

