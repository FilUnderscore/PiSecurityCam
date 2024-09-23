from datetime import datetime

class Database:
    def select():
        pass

    def list(self):
        pass

    def insert(self, table, data):
        pass

    def does_table_exist(self, table):
        pass

    def get_db_type(self, data):
        if isinstance(data, str):
            return "VARCHAR(255)"
        elif isinstance(data, int):
            return "INT"
        elif isinstance(data, datetime):
            return "DATETIME"