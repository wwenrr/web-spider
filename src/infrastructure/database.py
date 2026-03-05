from peewee import SqliteDatabase

from infrastructure.constants.db import DB_DIR_PATH, DB_FILE_PATH

DB_DIR_PATH.mkdir(parents=True, exist_ok=True)
database = SqliteDatabase(str(DB_FILE_PATH))
