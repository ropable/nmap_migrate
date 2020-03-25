# nmpspecies data migrator

A minimal Django project to migrate data from the Department's NMAP.NMPSPECIES
Oracle database to a new PostgreSQL home.

# Migrating data from Oracle to PostgreSQL

Requirements:

* Python 2.7 (to accomodate Django 1.11)
* Oracle instant client
* Django 1.11.*
* cx_Oracle

Notes:

* Remember to set the LD_LIBRARY_PATH environment variable to allow cx_Oracle
to utilise the system Oracle client.
