from db.sqlite_database import SqliteDatabase
from camera import DebugCamera
from picamera import PiCamera, MotionPiCamera
from app import App
from webserver import Webserver
from db.database_with_backup import DatabaseWithBackup
from db.mysql_database import MySQLDatabase
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--debug', action='store_true')
parser.add_argument('--no-motion', action='store_true')
args = parser.parse_args()

main_database = MySQLDatabase('localhost', 'test', 'password', 'test')
backup_database = SqliteDatabase('test.db')
database = DatabaseWithBackup(main_database, backup_database)

camera = None

if args.debug:
    camera = DebugCamera()
elif args.no_motion:
    camera = PiCamera()
else:
    camera = MotionPiCamera(database)

app = App(camera, database)
webserver = Webserver(app)
