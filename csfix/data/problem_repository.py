from datetime import datetime
from typing import TypeAlias

from csfix.data.repository import Repository
from csfix.data.sqlite_database import SQLiteDatabase
from csfix.model.problem import Problem

# If using queries where we dynamically construct a WHERE ... NOT IN ... clause, we
# can't construct the clause with more than 999 elements, so we chunk this.
LIST_CHUNK_SIZE = 999

ProblemTuple: TypeAlias = tuple[str, str, str, str, datetime]


def problem_to_tuple(problem: Problem) -> ProblemTuple:
    return (
        problem.tool_name,
        problem.file,
        problem.location,
        problem.description,
        problem.discovery_time,
    )


def tuple_to_problem(t: ProblemTuple) -> Problem:
    return Problem(
        tool_name=t[0],
        file=t[1],
        location=t[2],
        description=t[3],
        discovery_time=t[4],
    )


class ProblemRepository(Repository):
    def __init__(self, database: SQLiteDatabase):
        super().__init__(database)

        self._database.connection.executescript("""
            BEGIN;
            CREATE TABLE IF NOT EXISTS problems (
                tool_name VARCHAR(16),
                file TEXT,
                location TEXT,
                description TEXT,
                discovery_time TIMESTAMP,
                PRIMARY KEY (tool_name, file, location, description)
            );
            COMMIT;
        """)

    def get_all(self) -> list[Problem]:
        cursor = self._database.connection.cursor()
        cursor.execute("SELECT * FROM problems")
        results = cursor.fetchall()
        return [tuple_to_problem(t) for t in results]

    def get_by_file(self, file: str) -> list[Problem]:
        cursor = self._database.connection.cursor()
        cursor.execute("SELECT * FROM problems WHERE file = ?", (file,))
        results = cursor.fetchall()
        return [tuple_to_problem(t) for t in results]

    def exists_by_file_and_tool_name_after(
        self, file: str, tool_name: str, after_time: datetime
    ) -> bool:
        cursor = self._database.connection.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM problems "
            "WHERE file = ? AND tool_name = ? AND discovery_time >= ?",
            (file, tool_name, after_time),
        )
        (count,) = cursor.fetchone()
        return count > 0

    def delete_by_file_and_tool_name_before(
        self, file: str, tool_name: str, before_time: datetime
    ) -> int:
        connection = self._database.connection
        cursor = connection.cursor()
        cursor.execute(
            "DELETE FROM problems "
            "WHERE file = ? AND tool_name = ? AND discovery_time < ?",
            (file, tool_name, before_time),
        )
        connection.commit()
        return cursor.rowcount

    def delete_by_not_in_file_list(self, files: list[str]) -> int:
        connection = self._database.connection
        cursor = connection.cursor()
        total_row_count = 0

        for start_index in range(0, len(files), LIST_CHUNK_SIZE):
            files_chunk = files[start_index : start_index + LIST_CHUNK_SIZE]
            placeholders = ",".join(["?"] * len(files_chunk))
            query = f"DELETE FROM problems WHERE file NOT IN ({placeholders})"
            cursor.execute(query, files_chunk)
            connection.commit()
            total_row_count += cursor.rowcount

        return total_row_count

    def insert_many(self, problems: list[Problem]) -> None:
        problem_tuples = [problem_to_tuple(problem) for problem in problems]
        connection = self._database.connection
        connection.executemany(
            "INSERT INTO problems VALUES(?, ?, ?, ?, ?)", problem_tuples
        )
        connection.commit()
