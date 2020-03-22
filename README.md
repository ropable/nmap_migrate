# nmpspecies data transfer

A minimal Django project to copy data from the Department's NMAP.NMPSPECIES
Oracle database to a new PostgreSQL home.

Requirements:

* Python 2.7
* Oracle instant client
* cx_Oracle library

Notes:

* Remember to set the LD_LIBRARY_PATH environment variable to allow cx_Oracle
to utilise the system Oracle client.
