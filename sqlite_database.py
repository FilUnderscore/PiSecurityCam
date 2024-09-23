from database import Database
from util import CSSBuilder
import sqlite3

class SqliteDatabase(Database):
    def __init__(self, file_path):
        self.conn = sqlite3.connect(file_path)
        self.cursor = self.conn.cursor()

    def fetch(self, table, query):
        entries = []
        data = {}
        table_data = self.cursor.execute("PRAGMA table_info(" + table + ");").fetchall()

        # Returns data describing the table, in order:
        # cid | name | type | notnull | dflt_value | pk

        rows = self.cursor.execute(query).fetchall()

        for row in rows:
            for column in range(0, len(row)):
                data[table_data[column][1]] = row[column]
            
            entries.append(data)
        
        return entries

    def select(self, table, columns, value_query):
        return self.fetch(table, "SELECT " + columns + " FROM " + table + " WHERE " + value_query + ";")

    def list(self, table):
        return self.fetch(table, "SELECT * FROM " + table + ";")

    def create_table(self, table, data):
        columns_str_builder = CSSBuilder()

        for column_key in data:
            columns_str_builder.add_entry(column_key).extend_entry(self.get_db_type(data[column_key]))

        self.cursor.execute("CREATE TABLE " + table + " (" + columns_str_builder.build() + ");")
        self.conn.commit()

        print("SqliteDatabase: Created new table '" + table + "'")

    def insert(self, table, data):
        if not self.does_table_exist(table):
            self.create_table(table, data)

        keys_str_builder = CSSBuilder()

        for key in data:
            keys_str_builder.add_entry(key)
        
        values_str_builder = CSSBuilder()

        for key in data:
            values_str_builder.add_entry('\'' + data[key] + '\'')

        self.cursor.execute("INSERT INTO " + table + " (" + keys_str_builder.build() + ") VALUES (" + values_str_builder.build() + ")")
        self.conn.commit()

        print("SqliteDatabase: Inserted row into the '" + table + "' table.")

    def does_table_exist(self, table):
        try:
            tables = self.cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='" + table + "';").fetchone()
            return tables[0] != 0
        except:
            print("SqliteDatabase: An error occurred while attempting to check whether the table " + table + " exists.")

            return False