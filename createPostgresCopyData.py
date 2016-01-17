#!/usr/bin/env python3

"""
This script creates a data file for the 'trips' database table 
by processing the CSV file from Capital Bikeshare (CaBi). The
resulting output is suitable for the PostgreSQL COPY command,
which can then be used to populate the database table.

COPY trips (duration, start_time,
 stop_time, start_station_id,
 stop_station_id, bike_id,
  member_type_id)
 FROM '/home/john/github/bikeshare/data.csv';
"""
import psycopg2
import sys
import csv

import logging
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - %(message)s')
  
def createMemberDict(conn):
  """build a dictionary of memberType IDs from database"""
  memberDict = {}
  with conn:
    with conn.cursor() as cur:
      cur.execute("SELECT id, type FROM member_types")
      rows = cur.fetchall()
      for row in rows:
        (memberId, typeName) = row
        memberDict[typeName] = memberId
  return memberDict

def createDataFromCsv(inFile, outFile):
  dataFile = open(outFile, 'w', newline='')
  writer = csv.writer(dataFile,delimiter='\t')
  reader = csv.reader(open(inFile,newline=''),delimiter=',')
  # skip header row, but make sure it has 9 columns
  header = next(reader)
  if len(header) != 9:
    print("Unexpected format")
    print(header)
    sys.exit(1)

  # Sample CSV line in 9 column format
  """
  Duration (ms),Start date,End date,Start station number,
  Start station,End station number,End station,Bike #, Member type
  257866,7/1/2015 0:00,7/1/2015 0:04,31116,California St & Florida Ave NW,31117,15th & Euclid St  NW,W21516,Registered
  """

  # only care about duration, times, stations, bike, and member type

  try:
    conn = psycopg2.connect(dbname='gisdb', user='gisuser',
                            password='gis')
  except:
    print("Cannot connect to database")
    sys.exit(1)

  memberDict = createMemberDict(conn)

  line = 0
  for row in reader:
    (duration, start_date, stop_date, 
    start_station, start_station_name,
    stop_station, stop_station_name,
    bike, member_type) = row

    bikeId = bike[1:] # drop leading letter W
    memberId = memberDict[member_type]
    outRow = [duration, start_date, stop_date, start_station, stop_station, bikeId, memberId]
    writer.writerow(outRow)  

    if line % 10000 == 0:
      logging.debug(row)
    line += 1
  dataFile.close()
  return
  
if __name__ == "__main__":
  try:
    inFile = sys.argv[1]
  except:
    inFile = "trips.csv"
  try:
    outFile = sys.argv[2]
  except:
    outFile = "data.csv"

  createDataFromCsv(inFile, outFile)
  


