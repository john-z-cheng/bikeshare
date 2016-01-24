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

-- calculate the distances
update trip_pairs set distance=sq.distance
FROM (select tp.id as id,
 st_distance_sphere(x.geom, y.geom) as distance,
 tp.start_id, tp.stop_id 
from trip_pairs tp, stations x, stations y
where x.id=tp.start_id and y.id=tp.stop_id) as sq
where trip_pairs.start_id=sq.start_id and trip_pairs.stop_id=sq.stop_id;

-- associate the reverse trip to the forward trip
update trip_pairs set reverse_pair_id=x.rp_id
FROM (select tp.id as id, rp.id as rp_id
from trip_pairs tp, trip_pairs rp
where tp.start_id=rp.stop_id and tp.stop_id=rp.start_id) x
where x.id=trip_pairs.id;

DROP TABLE IF EXISTS trip_stats;
CREATE TABLE trip_stats (
  id SERIAL PRIMARY KEY,
  trip_pair_id integer REFERENCES trip_pairs (id),
  conditions text,
  sample_size integer,
  stat_name text,
  stat_value double precision
  );
  
