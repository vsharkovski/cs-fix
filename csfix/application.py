import logging
from pathlib import Path

from dotenv import load_dotenv

from csfix.constants import (
    DATA_DIRECTORY_NAME,
    DATABASE_FILE_NAME,
    ENV_DATA_DIRECTORY,
    ENV_OPENAI_API_KEY,
    ENV_OPENAI_MODEL,
)
from csfix.data.problem_repository import ProblemRepository
from csfix.data.scan_status_repository import ScanStatusRepository
from csfix.data.sqlite_database import SQLiteDatabase
from csfix.llm.openai_client import OpenAIClient
from csfix.service.problem_service import ProblemService
from csfix.service.scan_service import ScanService
from csfix.service.suggestion_service import SuggestionService
from csfix.service.tool_service import ToolService
from csfix.util import get_env_var_or_throw


class Application:
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG)

        load_dotenv()

        data_parent_directory_str = get_env_var_or_throw(ENV_DATA_DIRECTORY)
        data_parent_directory = Path(data_parent_directory_str).resolve()
        self._data_directory = None
        self._initialize_data_directory(data_parent_directory)

        database_directory = self._data_directory / DATABASE_FILE_NAME
        database = SQLiteDatabase(database_directory)
        database.connect()

        scan_status_repository = ScanStatusRepository(database)
        problem_repository = ProblemRepository(database)

        self._problem_service = ProblemService(problem_repository)

        self._tool_service = ToolService()

        self._scan_service = ScanService(
            self._tool_service, self._problem_service, scan_status_repository
        )

        openai_api_key = get_env_var_or_throw(ENV_OPENAI_API_KEY)
        openai_model = get_env_var_or_throw(ENV_OPENAI_MODEL)
        llm_client = OpenAIClient(openai_api_key, openai_model)
        self._suggestion_service = SuggestionService(llm_client)

    def scan(self, directory: Path, tool_codes: list[str]) -> None:
        self._problem_service.delete_problems_for_nonexistent_files(directory)
        self._scan_service.scan(directory, tool_codes)

    def show_problems(self, directory) -> None:
        self._problem_service.show_problems(directory)

    def get_suggestions(self, file_path: Path) -> None:
        raise NotImplementedError

    def _initialize_data_directory(self, data_parent_directory: Path) -> None:
        if data_parent_directory.exists() and not data_parent_directory.is_dir():
            raise ValueError(
                "Given data directory path is not a directory: "
                f'"{data_parent_directory}"'
            )

        data_directory = data_parent_directory / DATA_DIRECTORY_NAME
        self._data_directory = data_directory
        if data_directory.exists() and not data_directory.is_dir():
            raise ValueError(
                f'Already exists but is not a directory: "{data_directory}"'
            )

        data_directory.mkdir(parents=True, exist_ok=True)
