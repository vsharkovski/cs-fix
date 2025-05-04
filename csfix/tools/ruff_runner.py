import subprocess
from datetime import datetime
from pathlib import Path
from csfix.model.problem import Problem
from csfix.tools.tool_runner import ToolRunner

class RuffRunner(ToolRunner):
    def run(self, file: Path) -> list[Problem]:
        cmd = ["ruff", "check", str(file)] 
        result = subprocess.run(cmd, text=True, capture_output=True)
        ruff_output = result.stdout or ""
        if result.returncode == 0 and not ruff_output:
            return []

        problems: list[Problem] = []
        for line in ruff_output.splitlines():
            if line.strip():  
                parts = line.split(":")
                if len(parts) >= 4:
                    line_num = parts[1]
                    column_num = parts[2]
                    code = parts[3].strip()
                    message = ":".join(parts[4:]).strip()
                    location = f"{line_num}:{column_num}"
                    full_message = f"{code} {message}"

                    problems.append(
                        Problem(
                            tool_name=self.name,
                            file=str(file),
                            location=location,
                            description=full_message,
                            discovery_time=datetime.now(),
                        )
                    )
        return problems
