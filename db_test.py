from sqlite_database import SqliteDatabase
from datetime import datetime

db = SqliteDatabase("test.db")
db.insert("test_table", { 'test': 'test123', 'test_date': datetime.now().strftime("%d/%m/%Y %H:%M:%S") })
print(db.list("test_table"))