# nmpspecies data migrator

A minimal Django project to migrate data from the Department's NMAP.NMPSPECIES
Oracle database to a new PostgreSQL home.

Requirements:

* Python 2.7
* Oracle instant client
* cx_Oracle library

Notes:

* We're using Django 1.11.* because that talks to the Oracle database fine.
* Remember to set the LD_LIBRARY_PATH environment variable to allow cx_Oracle
to utilise the system Oracle client.
