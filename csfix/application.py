import logging
from pathlib import Path

from dotenv import load_dotenv

from csfix.constants import (
    DATA_DIRECTORY_NAME,
    DATABASE_FILE_NAME,
    ENV_DATA_DIRECTORY,
    ENV_GROQ_API_KEY,
    ENV_GROQ_MODEL,
)
from csfix.data.problem_repository import ProblemRepository
from csfix.data.scan_status_repository import ScanStatusRepository
from csfix.data.sqlite_database import SQLiteDatabase
from csfix.llm.groq_client import GroqClient
from csfix.service.problem_service import ProblemService
from csfix.service.scan_service import ScanService
from csfix.service.suggestion_service import SuggestionService
from csfix.service.tool_service import ToolService
from csfix.util import get_env_var_or_throw


class Application:
    def __init__(self):
        # Logging configuration
        logging.basicConfig(level=logging.INFO)

        # Disable debug logs from http libraries
        logging.getLogger("httpx").setLevel(logging.WARNING)
        logging.getLogger("httpcore").setLevel(logging.WARNING)

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

        api_key = get_env_var_or_throw(ENV_GROQ_API_KEY)
        api_model = get_env_var_or_throw(ENV_GROQ_MODEL)
        llm_client = GroqClient(api_key, api_model)
        self._suggestion_service = SuggestionService(llm_client)

    def scan(self, directory: Path, tool_codes: list[str]) -> None:
        self._problem_service.delete_problems_for_nonexistent_files(directory)
        self._scan_service.scan(directory, tool_codes)

    def show_problems(self, directory) -> None:
        self._problem_service.show_problems(directory)

    def get_suggestions(self, file_path: Path) -> None:
        problems = self._problem_service.get_problems_for_file(file_path)
        if not problems:
            print(f"No problems found for file: {file_path}")
            return

        # Get file content
        file_content = file_path.read_text()

        # Get suggestions from LLM for each problem
        for problem in problems:
            print(f"\nProblem at {problem.location}: {problem.description}")
            print("Suggested fix:")
            try:
                suggestion = self._suggestion_service.get_suggestion(
                    file_content, problem
                )
                print(suggestion)
            except Exception as e:
                print(f"Error getting suggestion: {str(e)}")
            print("-" * 80)

    def apply_fixes(self, file_path: Path) -> None:
        """Apply fixes to a file using LLM suggestions"""
        problems = self._problem_service.get_problems_for_file(file_path)
        if not problems:
            print(f"No problems found for file: {file_path}")
            return

        print(f"Applying fixes to {file_path}...")

        # Apply fixes for each problem
        for problem in problems:
            print(f"Fixing: {problem.description} at {problem.location}")
            success, message = self._suggestion_service.get_and_apply_fix(
                file_path, problem
            )

            if success:
                print(f"✓ {message}")
            else:
                print(f"✗ {message}")

        # Re-scan the file to check if problems were fixed
        print("\nRe-scanning file to verify fixes...")
        for tool_code in ["ruff"]:  # Add other tools as needed
            tool = self._tool_service.get_tool_by_code(tool_code)
            self._scan_service._scan(file_path, tool)

        # Check if there are still problems
        remaining_problems = self._problem_service.get_problems_for_file(file_path)
        if remaining_problems:
            print(f"\nRemaining problems ({len(remaining_problems)}):")
            for problem in remaining_problems:
                print(f"- {problem.description} at {problem.location}")
        else:
            print("\nAll problems fixed successfully!")

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
