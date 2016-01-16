#!/usr/bin/env python3

"""
This script populates the 'stations' database table using an XML
file from Capital Bikeshare. That XML file should be downloaded and
renamed 'bikeStations.xml'. That database table should be empty (to
avoid an exception due to inserting row with duplicate key).
"""

import logging
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - %(message)s')

import psycopg2
import sys

conn = psycopg2.connect(dbname='gisdb',user='gisuser',password='gis')
cur = conn.cursor()

import xml.etree.cElementTree as ET

tree = ET.parse('bikeStations.xml')

# These are the children of interest
childTags = ['name','terminalName','lat','long',
'nbBikes','nbEmptyDocks']
falseStatusTags = ['locked','temporary']
trueStatusTags = ['installed','public']
stations = tree.findall('station')
for station in stations:
  print("STATION")
  stationName = station.find('name').text
  stationId = station.find('terminalName').text
  lat = station.find('lat').text
  lon = station.find('long').text
  fullDocks = station.find('nbBikes').text
  emptyDocks = station.find('nbEmptyDocks').text
  dockQty = int(fullDocks) + int(emptyDocks) 
  logging.debug('name: ' + stationName)
  logging.debug('id: ' + stationId)
  logging.debug('lat: ' + lat)
  logging.debug('lon: ' + lon)
  logging.debug('docks: ' + str(dockQty))
  for child in station:
    if child.tag in trueStatusTags:
      if child.text != 'true':
        print(child.tag, child.text)
    if child.tag in falseStatusTags:
      if child.text != 'false':
        print(child.tag, child.text)
        
  cur.execute("""INSERT INTO stations (id, name, lat, lon, dock_qty, geom) VALUES (%s, %s, %s, %s, %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326))""", (stationId, stationName, lat, lon, dockQty, lon, lat))
conn.commit()

