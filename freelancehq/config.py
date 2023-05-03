import os

DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
HOST = os.environ.get('HOST')
DB_NAME = os.environ.get('DB_NAME')


db_credentials = {
    'user': DB_USER, 
    'password': DB_PASSWORD,
    'host': HOST,
    'database': DB_NAME
}