# nmpspecies data migrator

A minimal Django project to migrate data from the Department's NMAP.NMPSPECIES
Oracle database to a new PostgreSQL home. This project is only required to
migrate the data, after which time the `naturemap` application will be moved to
a newer project environment.

# Migrating data from Oracle to PostgreSQL

## Requirements

* Python 2.7 (to accommodate Django 1.11)
* Oracle instant client installed on host
* Django 1.11.*
* cx_Oracle

## Instructions

1. Install the project.
2. Define a `.env` file that includes Oracle username, password and connect
   descriptor (as well as a database URL to the destination database).
3. Start a shell session and run:
```
from naturemap2 import utils
utils.import_nmap_data()
```

The import will take some time to complete.

Notes:

* The `ORACLE_DESCRIPTOR` env variable will be something like
`(DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)(HOST=hostname.domain)(PORT=1521)))(CONNECT_DATA=(SERVICE_NAME=service.name)(SERVER=DEDICATED)))`.
Check a current `tnsnames.ora` file.
* The `ORACLE_PASSWORD` env var may need special characters (such as `$`) escaped with a backslash.
* Remember to set the `LD_LIBRARY_PATH` environment variable to allow cx_Oracle
  to utilise the system Oracle client.
* The `nmpspecies` application is the read-only generated data model allowing
  the legacy Oracle database to be queried, transformed and loaded into a new
  PostgreSQL database.
* The `naturemap2` application is the manually-built data model to manage the
  migrated data. The data model remains largely unchanged from the source, with
  the exception of longer field names, type constraints and some other
  conveniences provided by Django (such as descriptive help text).
