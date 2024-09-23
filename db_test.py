from sqlite_database import SqliteDatabase

db = SqliteDatabase("test.db")
db.insert("test_table", { 'test': 'test123' })