from dataclasses import dataclass
from datetime import datetime


@dataclass
class ScanStatus:
    file: str
    tool_name: str
    scan_time: datetime
    problem_count: int
