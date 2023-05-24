import mysql.connector
from freelancehq import config

class DBConnection:
    def __init__(self):
        self.cnx = mysql.connector.connect(**config.db_credentials)
        self.cursor = self.cnx.cursor()

    def execute(self, sql, values):
        try:
            self.cursor.execute(sql, values)
        except Exception as e:
            print(e)
            self.close_cnx()


    def close_cnx(self):
        self.cursor.close()
        self.cnx.close()

    def commit(self):
        self.cnx.commit()
