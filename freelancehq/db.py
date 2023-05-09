import mysql.connector
from freelancehq import config

class DBConnection:
    def __init__(self):
        self.cnx = mysql.connector.connect(**config.db_credentials)
        self.cursor = self.cnx.cursor()

    def execute(self, sql, values):
        self.cursor.execute(sql, values)


    def close_cnx(self):
        self.cursor.close()
        self.cnx.close()
