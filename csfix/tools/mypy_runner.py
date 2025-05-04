import re
import subprocess
from datetime import datetime
from pathlib import Path

from csfix.model.problem import Problem
from csfix.tools.tool_runner import ToolRunner


LINE_RE = re.compile(
    r"""
    ^
    (?P<file>.+?)         
    :(?P<line>\d+)       
    (?::(?P<col>\d+))?   
    \s*:\s*
    (?P<severity>\w+)    
    \s*:\s*
    (?P<msg>.+)           
    $
    """,
    re.VERBOSE,
)

class MypyRunner(ToolRunner):

    name = "mypy"
    def run(self, file: Path) -> list[Problem]:
        # Execute mypy
        cmd = ["mypy", str(file)]
        result = subprocess.run(cmd, text=True, capture_output=True)
        output = result.stdout or ""
        print(output)
        problems: list[Problem] = []
        for raw in output.splitlines():
            match = LINE_RE.match(raw)
            if not match:
                continue

            file_path = str(file)
            line_num = match.group("line")
            col_num = match.group("col") or "0"
            severity = match.group("severity")
            message = match.group("msg").strip()

            location = f"{line_num}:{col_num}"
            description = f"{severity} {message}"

            problems.append(
                Problem(
                    tool_name=self.name,
                    file=file_path,
                    location=location,
                    description=description,
                    discovery_time=datetime.now(),
                )
            )

        return problems
