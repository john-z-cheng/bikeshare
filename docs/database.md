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
The actual analysis to be done on the trip data is TBD, but generally expect to aggregate the data somehow. So a fairly flexible schema could have a table with "statistical measures" and another to hold the calculated values for a given station(s). The table with the station, the measure id, and the measure value could grow in the number of rows as new measures are calculated and inserted. Depending on how data is sliced and diced (and then presented), there may be multiple tables that are similar in structure whose contents might be aggregated over different time periods.

The SQL file create these tables is **analysis_ddl.sql**, separate from the other SQL file because it will probably be changed much more often as I think of new analyses to be tried.

