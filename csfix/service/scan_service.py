from pathlib import Path

from csfix.service.problem_service import ProblemService
from csfix.service.tool_service import ToolService


class ScanService:
    def __init__(self, tool_service: ToolService, problem_service: ProblemService):
        self._tool_service = tool_service
        self._problem_service = problem_service

    def scan(self, directory: Path, tool_codes: list[str]) -> None:
        pass
