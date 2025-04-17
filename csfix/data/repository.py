from abc import ABC

from csfix.data.sqlite_database import SQLiteDatabase


class Repository(ABC):
    def __init__(self, database: SQLiteDatabase):
        self._database = database
