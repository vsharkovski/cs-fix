from datetime import datetime
from pathlib import Path

from csfix.model.problem import Problem
from csfix.tools.tool_runner import ToolRunner


class RuffRunner(ToolRunner):
    def run(self, file: Path) -> list[Problem]:
        file_str = str(file)
        return [
            Problem(self.name, file_str, "nowhere", "dummy problem", datetime.now())
        ]
