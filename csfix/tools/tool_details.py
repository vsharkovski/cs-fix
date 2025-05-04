from dataclasses import dataclass
from typing import Type

from csfix.tools.ruff_runner import RuffRunner
from csfix.tools.mypy_runner import MypyRunner
from csfix.tools.tool_runner import ToolRunner


@dataclass
class ToolDetails:
    name: str
    description: str
    code: str  # Code used for CLI to include the tool in scanning.
    runner_type: Type[ToolRunner]

    def create_runner(self) -> ToolRunner:
        return self.runner_type(self.name)


TOOLS = [
    ToolDetails(
        name="Ruff",
        description="Python linter and code formatter",
        code="ruff",
        runner_type=RuffRunner,
    ),
     ToolDetails(
        name="mypy",
        description="Python Type checking",
        code="mypy",
        runner_type=MypyRunner,
    )
]
