from db.sqlite_database import SqliteDatabase
from camera import DebugCamera
from app import App
from webserver import Webserver

app = App(DebugCamera(), SqliteDatabase('test.db'))
webserver = Webserver(app)