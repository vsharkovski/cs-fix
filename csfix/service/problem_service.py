from pathlib import Path

from csfix.data.problem_repository import ProblemRepository


class ProblemService:
    def __init__(self, problem_repository: ProblemRepository):
        self._problem_repository = problem_repository

    def show_problems(self, directory: Path) -> None:
        pass
