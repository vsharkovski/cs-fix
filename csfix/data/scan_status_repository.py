from csfix.data.repository import Repository
from csfix.data.sqlite_database import SQLiteDatabase
from csfix.model.scan_status import ScanStatus


class ScanStatusRepository(Repository):
    def __init__(self, database: SQLiteDatabase):
        super().__init__(database)

        self._database.connection.executescript("""
            BEGIN;
            CREATE TABLE IF NOT EXISTS scan_statuses (
                file TEXT,
                tool_name VARCHAR(16),
                scan_time INTEGER,
                problem_count INTEGER,
                PRIMARY KEY (file, tool_name)
            );
            COMMIT;
        """)

    def get_all(self):
        cursor = self._database.connection.cursor()
        cursor.execute("SELECT * FROM scan_statuses")
        return cursor.fetchall()

    def get_by_file_and_tool_name(self, file: str, tool_name: str) -> ScanStatus | None:
        cursor = self._database.connection.cursor()
        cursor.execute(
            "SELECT * FROM scan_statuses WHERE file = ? AND tool_name = ?",
            (file, tool_name),
        )
        result = cursor.fetchone()
        if not result:
            return None
        return ScanStatus(
            file=result[0],
            tool_name=result[1],
            scan_time=result[2],
            problem_count=result[3],
        )

    def delete_by_file_and_tool_name(self, file: str, tool_name: str) -> int:
        connection = self._database.connection
        cursor = connection.cursor()
        cursor.execute(
            "DELETE FROM scan_statuses WHERE file = ? AND tool_name = ?",
            (file, tool_name),
        )
        connection.commit()
        return cursor.rowcount

    def insert(self, scan_status: ScanStatus) -> None:
        connection = self._database.connection
        connection.execute(
            "INSERT INTO scan_statuses VALUES(?, ?, ?, ?)",
            (
                scan_status.file,
                scan_status.tool_name,
                scan_status.scan_time,
                scan_status.problem_count,
            ),
        )
        connection.commit()
