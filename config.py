import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database
  
# Just change the names of your database and credentials  and all to connect to your local system

DATABASE_NAME='fyyur'
username='postgres'
password='123456'
url='localhost:5432'
SQLALCHEMY_DATABASE_URI = f'postgresql://{username}:{password}@{url}/{DATABASE_NAME}'
