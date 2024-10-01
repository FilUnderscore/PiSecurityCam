from db.database import Database

class DatabaseWithBackup(Database):
    def __init__(self, main_db, backup_db):
        self.main_db = main_db
        self.backup_db = backup_db

    def get_db(self):
        # Check if main DB is down, if so pull from backup DB
        database = None

        if self.main_db.online():
            database = self.main_db
        else:
            database = self.backup_db
        
        return database

    def select(self, table, columns, whereClauseStr):
        return self.get_db().select(table, columns, whereClauseStr)

    def list(self, table):
        return self.get_db().list(table)

    def insert(self, table, data):
        self.main_db.insert(table, data)
        self.backup_db.insert(table, data)
