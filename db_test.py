from db.sqlite_database import SqliteDatabase
from db.mysql_database import MySQLDatabase
from db.database_with_backup import DatabaseWithBackup
from datetime import datetime

backup_db = SqliteDatabase("test.db")
main_db = MySQLDatabase("localhost", "test", "password", "test")
db = DatabaseWithBackup(main_db, backup_db)

db.insert("test_table", { 'test': 'test123', 'test_date': datetime.now().strftime("%d/%m/%Y %H:%M:%S") })
print(db.list("test_table"))
print(db.select("test_table", ["test_date"], "test = 'test123'"))
