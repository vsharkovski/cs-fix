from csfix.data.repository import Repository


class ProblemRepository(Repository):
    def get_all(self):
        cursor = self._database.connection.cursor()
        cursor.execute("SELECT * FROM problems")
        return cursor.fetchall()

    def get_by_file(self, file: str):
        return []
