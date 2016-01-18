DROP TABLE IF EXISTS trip_pairs;

-- Table for start and stop station trip pairs
CREATE TABLE trip_pairs (
  id SERIAL PRIMARY KEY,
  start_id integer REFERENCES stations (id),
  stop_id integer REFERENCES stations (id),
  reverse_pair_id integer REFERENCES trip_pairs (id),
  distance double precision
  );

INSERT INTO trip_pairs (start_id, stop_id) 
SELECT DISTINCT start_id, stop_id FROM trips;
