from db.sql_database import SQLDatabase

import pymysql

class MySQLDatabase(SQLDatabase):
    def __init__(self, host, username, password, database):
        SQLDatabase.__init__(self, pymysql.connect(host=host, user=username, password=password, db=database))

    def get_table_data(self, table):
        cursor = self.conn.cursor()
        cursor.execute("DESCRIBE " + table + ";")
        table_data = cursor.fetchall()

        table_col_list = []

        for column in range(0, len(table_data)):
            col_data = {
                "name": table_data[column][0]
            }

            table_col_list.append(col_data)

        return table_col_list

    def create_table(self, table, data):
        SQLDatabase.create_table(self, table, data)

        print("MySQLDatabase: Created new table '" + table + "'")

    def insert(self, table, data):
        SQLDatabase.insert(self, table, data)

        print("MySQLDatabase: Inserted row into the '" + table +"'")
    
    def does_table_exist(self, table):
        cursor = self.conn.cursor()
        table = cursor.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_name = '" + table + "';")
        return cursor.fetchone()[0] == 1
    
    def execute_fetch(self, statement):
        cursor = self.conn.cursor()
        cursor.execute(statement)
        return cursor.fetchall()
    
    def online(self):
        try:
            self.conn.ping()
            return self.conn.open
        except:
            return False
