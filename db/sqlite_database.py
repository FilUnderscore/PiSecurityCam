from db.sql_database import SQLDatabase
import sqlite3

class SqliteDatabase(SQLDatabase):
    def __init__(self, file_path):
        SQLDatabase.__init__(self, sqlite3.connect(file_path, check_same_thread=False))

    def get_table_data(self, table):
        cursor = self.conn.cursor()
        table_data = cursor.execute("PRAGMA table_info(" + table + ");").fetchall()

        # Returns data describing the table, in order:
        # cid | name | type | notnull | dflt_value | pk

        table_col_list = []
        
        for column in range(0, len(table_data)):
            col_data = {
                "name": table_data[column][1]
            }

            table_col_list.append(col_data)
        
        return table_col_list

    def create_table(self, table, data):
        SQLDatabase.create_table(self, table, data)

        print("SqliteDatabase: Created new table '" + table + "'")

    def insert(self, table, data):
        SQLDatabase.insert(self, table, data)

        print("SqliteDatabase: Inserted row into the '" + table + "' table.")

    def does_table_exist(self, table):
        cursor = self.conn.cursor()

        try:
            tables = cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='" + table + "';").fetchone()
            return tables[0] != 0
        except:
            print("SqliteDatabase: An error occurred while attempting to check whether the table " + table + " exists.")

            return False
    
    def execute_fetch(self, statement):
        cursor = self.conn.cursor()
        return cursor.execute(statement).fetchall()
    
    def online(self):
        return True
