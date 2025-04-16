import os
from pathlib import Path

from dotenv import load_dotenv

from csfix.data.problem_repository import ProblemRepository
from csfix.data.sqlite_database import SQLiteDatabase
from csfix.llm.openai_client import OpenAIClient
from csfix.service.problem_service import ProblemService
from csfix.service.scan_service import ScanService
from csfix.service.suggestion_service import SuggestionService
from csfix.service.tool_service import ToolService


class Application:
    def __init__(self):
        load_dotenv()

        data_directory_str = os.environ.get()
        self.data_directory = Path(data_directory_str)
        self._initialize_data_directory()

        database = SQLiteDatabase(self.data_directory)
        problem_repository = ProblemRepository(database)

        self._problem_service = ProblemService(problem_repository)

        self._tool_service = ToolService()

        self._scan_service = ScanService(self._tool_service, self._problem_service)

        llm_client = OpenAIClient("", "")
        self._suggestion_service = SuggestionService(llm_client)

    def scan(self, directory: Path, tool_codes: list[str]) -> None:
        self._scan_service.scan(directory, tool_codes)

    def show_problems(self, directory) -> None:
        self._problem_service.show_problems(directory)

    def get_suggestions(self, file_path: Path) -> None:
        pass

    def _initialize_data_directory() -> None:
        pass
