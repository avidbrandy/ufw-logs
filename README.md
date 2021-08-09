# ufw-logs
This repository is for collecting UFW logs from the local machine and storing them in an assigned database.

This project uses a PostgreSQL database and Django. There is a config.ini file to connect to the database.

This is a simple script with a single function, located in ufw_logs/ufw_logs/parser.py


## Django & PostgreSQL Database
For help setting up Django with PostgreSQL, this guide can be followed even if you have little knowledge:
- https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-16-04

Django models are at ufw_logs/ufw_logs/models.py


## Configuration
ufw_logs/config.ini contains the settings for connecting to your database.
