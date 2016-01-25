# Database Design

**Postgresql** database is used because of its integration with GIS (i.e. *PostGIS*). Postgresql also has a JSON datatype which may be helpful for future integration/migration to a document-based datastore.

## Input Data
The main open data comes in two types of files.
* an XML file with bike station status
* CSV files with bike trips (released on quarterly year basis)

These two data will go into the main tables:
- stations
- trips

Additional tables for normalization are:
- jurisdictions
- member_types

The SQL file to create these tables is **gisddl.sql**
  
## Analysis Data
The actual analysis to be done on the trip data is TBD, but generally expect to aggregate the data somehow. There will be 3 tables:

**trip_pairs** contains the distinct start and stop stations for trips. It is based on actual trips taken. It also provides a table to store the calculation for their nominal distance.

**trip_quantity** contains the number of trips taken for each pair. By querying the database and saving these values, it will help provide filtering to limit statistical calculations only on more popular trips.

**trip_stats** is a table for holding various statistics. By using a column for stat_name and stat_value, it is flexible enough to hold new values without requiring a schema change.

Later, depending on how data is sliced and diced (and then presented), there may be purpose-designed tables to make it easier to retrieve precalculated results.

The SQL file create these tables is **analysis_ddl.sql**. In addition to DDL to create the tables, it also has DML to populate the trip_pairs ad trip_quantity tables (using INSERT ... SELECT statements).
