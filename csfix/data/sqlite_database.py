import sqlite3
from pathlib import Path
from typing import Optional

from csfix.exceptions import DatabaseNotConnectedError


class SQLiteDatabase:
    def __init__(self, db_path: Path):
        self._db_path = db_path
        self._connection: Optional[sqlite3.Connection] = None

    def __del__(self):
        if self._connection:
            self._connection.close()

    def connect(self) -> None:
        self._connection = sqlite3.connect(str(self._db_path))

    @property
    def connection(self) -> sqlite3.Connection:
        if not self._connection:
            raise DatabaseNotConnectedError()
        return self._connection
