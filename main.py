from db.sqlite_database import SqliteDatabase
from camera import DebugCamera
from app import App
from webserver import Webserver

app = App(DebugCamera(), SqliteDatabase('test_2.db'))
webserver = Webserver(app)