import logging
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional

from csfix.exceptions import DatabaseNotConnectedError


def adapt_datetime_epoch(val):
    """Adapt datetime.datetime to Unix timestamp."""
    return int(val.timestamp())


def convert_timestamp(val):
    """Convert Unix epoch timestamp to datetime.datetime object."""
    return datetime.fromtimestamp(int(val))


sqlite3.register_adapter(datetime, adapt_datetime_epoch)
sqlite3.register_converter("timestamp", convert_timestamp)


logger = logging.getLogger(__name__)


class SQLiteDatabase:
    def __init__(self, db_path: Path):
        self._db_path = db_path
        self._connection: Optional[sqlite3.Connection] = None

    def __del__(self):
        if self._connection:
            self._connection.close()

    def connect(self) -> None:
        logger.info(f"Using/creating SQLite database at: {self._db_path}")
        self._connection = sqlite3.connect(
            str(self._db_path), detect_types=sqlite3.PARSE_DECLTYPES
        )

    @property
    def connection(self) -> sqlite3.Connection:
        if not self._connection:
            raise DatabaseNotConnectedError
        return self._connection
