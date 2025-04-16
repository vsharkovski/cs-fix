from dataclasses import dataclass
from datetime import datetime


@dataclass
class Problem:
    # Tool which discovered the problem.
    tool_name: str

    discovery_time: datetime

    file: str  # Or Path
    location: str  # line numbers?
    description: str  # Problem details
