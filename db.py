from database import Database

class DB(Database):
    def __init__(self, main_db, backup_db):
        self.main_db = main_db
        self.backup_db = backup_db

    def select(self, table, columns, value_query):
        # TODO: Check if main DB is down, if so pull from backup DB

        return self.main_db.select(table, columns, value_query)

    def list(self):
        # TODO: Check if main DB is down, if so pull from backup DB

        return self.main_db.list()

    def insert(self, table, data):
        self.main_db.insert(table, data)
        self.backup_db.insert(table, data)