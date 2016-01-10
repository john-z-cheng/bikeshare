DROP TABLE IF EXISTS stations CASCADE;
DROP TABLE IF EXISTS jurisdictions CASCADE;
DROP TABLE IF EXISTS trips CASCADE;
DROP TABLE IF EXISTS member_types CASCADE;

CREATE TABLE jurisdictions (
  id SERIAL PRIMARY KEY,
  name text CONSTRAINT namechk CHECK (char_length(name) <= 255)
  );
  
CREATE TABLE stations (
  id integer PRIMARY KEY,
  name text CONSTRAINT namechk CHECK (char_length(name) <= 255),
  lat numeric,
  lon numeric,
  dock_qty integer,
  jurisdiction_id integer REFERENCES jurisdictions (id)
  );

SELECT AddGeometryColumn ('stations', 'geom', 4326, 'POINT', 2);
CREATE TABLE member_types (
  id SERIAL PRIMARY KEY,
  type text
  );

CREATE TABLE trips (
  id SERIAL PRIMARY KEY,
  duration integer,
  start_time TIMESTAMP,
  stop_time TIMESTAMP,
  start_station_id integer REFERENCES stations (id),
  stop_station_id integer REFERENCES stations (id),
  bike_id integer,
  member_type_id integer REFERENCES member_types (id)
  );
  
INSERT INTO member_types VALUES (DEFAULT,'Casual'),(DEFAULT,'Registered');
