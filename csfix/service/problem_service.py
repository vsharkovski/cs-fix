import logging
from datetime import datetime
from pathlib import Path

from prettytable import PrettyTable

from csfix.data.problem_repository import ProblemRepository
from csfix.model.problem import Problem
from csfix.tools.tool_details import ToolDetails
from csfix.util import glob_files_resolved

logger = logging.getLogger(__name__)


class ProblemService:
    def __init__(self, problem_repository: ProblemRepository):
        self._problem_repository = problem_repository

    def show_problems(self, directory: Path) -> None:
        files = glob_files_resolved(directory, "**/*.py")

        for file in files:
            problems = self._problem_repository.get_by_file(str(file))
            if not problems:
                continue

            table = PrettyTable()
            table.field_names = ["Tool", "Location", "Description"]
            for problem in problems:
                table.add_row(
                    [problem.tool_name, problem.location, problem.description]
                )

            print(f"{file}:")
            print(table)

    def delete_problems_for_nonexistent_files(self, directory: Path) -> None:
        files = glob_files_resolved(directory, "**/*.py")
        files_str = [str(file) for file in files]
        self._problem_repository.delete_by_not_in_file_list(files_str)

    def delete_problems_by_file_and_tool_before(
        self, file: Path, tool: ToolDetails, before_time: datetime
    ) -> None:
        self._problem_repository.delete_by_file_and_tool_name_before(
            str(file), tool.name, before_time
        )

    def insert_problems(self, problems: list[Problem]) -> None:
        self._problem_repository.insert_many(problems)

    def get_problems_for_file(self, file: Path) -> list[Problem]:
        return self._problem_repository.get_by_file(str(file))
