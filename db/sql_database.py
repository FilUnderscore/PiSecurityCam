from db.database import Database
from util import CSSBuilder

class SQLDatabase(Database):
    def __init__(self, conn):
        self.conn = conn

    def insert(self, table, data):
        if not self.does_table_exist(table):
            self.create_table(table, data)

        keys_str_builder = CSSBuilder()

        for key in data:
            keys_str_builder.add_entry(key)
        
        values_str_builder = CSSBuilder()

        for key in data:
            values_str_builder.add_entry('\'' + data[key] + '\'')

        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO " + table + " (" + keys_str_builder.build() + ") VALUES (" + values_str_builder.build() + ")")
        self.conn.commit()

        print("SqliteDatabase: Inserted row into the '" + table + "' table.")

    def fetch(self, table, columns, whereClauseStr):
        entries = []

        table_data = self.get_table_data(table)

        if len(columns) == 0:
            for column in range(0, len(table_data)):
                columns.append(table_data[column]["name"])

        columns_str_builder = CSSBuilder()

        for column in columns:
            columns_str_builder.add_entry(column)

        rows = self.execute_fetch("SELECT " + columns_str_builder.build() + " FROM " + table + whereClauseStr + ";")

        for row in rows:
            colIndex = 0
            data = {}

            for column in range(0, len(table_data)):
                if table_data[column]["name"] not in columns:
                    print('skip')
                    continue

                data[table_data[column]["name"]] = row[colIndex]
                colIndex += 1
            
            entries.append(data)
        
        return entries
    
    def select(self, table, columns, whereClauseStr):
        return self.fetch(table, columns, " WHERE " + whereClauseStr)

    def list(self, table):
        return self.fetch(table, [], "")

    def create_table(self, table, data):
        columns_str_builder = CSSBuilder()

        for column_key in data:
            columns_str_builder.add_entry(column_key).extend_entry(self.get_db_type(data[column_key]))

        cursor = self.conn.cursor()

        cursor.execute("CREATE TABLE " + table + " (" + columns_str_builder.build() + ");")
        self.conn.commit()
    
    def insert(self, table, data):
        if not self.does_table_exist(table):
            self.create_table(table, data)

        keys_str_builder = CSSBuilder()

        for key in data:
            keys_str_builder.add_entry(key)
        
        values_str_builder = CSSBuilder()

        for key in data:
            values_str_builder.add_entry('\'' + data[key] + '\'')

        cursor = self.conn.cursor()

        cursor.execute("INSERT INTO " + table + " (" + keys_str_builder.build() + ") VALUES (" + values_str_builder.build() + ")")
        self.conn.commit()

    def does_table_exist(self, table):
        pass
    
    def execute_fetch(self, statement):
        pass
