from attr import dataclass


@dataclass
class ToolDetails:
    name: str
    description: str

    # Code used for CLI to include the tool in scanning.
    code: str
