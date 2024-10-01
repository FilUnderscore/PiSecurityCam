from sqlite_database import SqliteDatabase
from mysql_database import MySQLDatabase
from datetime import datetime

#db = SqliteDatabase("test.db")
db = MySQLDatabase("localhost", "test", "password", "test")
db.insert("test_table", { 'test': 'test123', 'test_date': datetime.now().strftime("%d/%m/%Y %H:%M:%S") })
print(db.list("test_table"))
print(db.select("test_table", ["test_date"], "test = 'test123'"))
