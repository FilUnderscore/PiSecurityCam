from database import Database

import mysql.connector

class MySQLDatabase(Database):
    def __init__(self, host, username, password, database):
        self.conn = mysql.connector.connect(host=host, username=username, password=password, database=database)

    def select(self, table, columns, value_query):
        pass

    def list(self):
        pass

    def insert(self, table, data):
        self.cursor.execute("")
        self.conn.commit()

        print("MySQLDatabase: Inserted row into the '" + table +"'")
    
    def does_table_exist(self, table):
        cursor = self.conn.cursor()
        table = cursor.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_name = '" + table + "';")
        return cursor.fetchone()[0] == 1