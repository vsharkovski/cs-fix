from csfix.exceptions import ToolNotFoundError
from csfix.tools.tool_details import TOOLS, ToolDetails


class ToolService:
    def __init__(self):
        self._tool_code_to_tool = {tool.code.lower(): tool for tool in TOOLS}

    def get_tool_by_code(self, code: str) -> ToolDetails:
        code_lower = code.lower()
        tool = self._tool_code_to_tool.get(code_lower)
        if not tool:
            raise ToolNotFoundError(f"Unrecognized tool code: {code_lower}")
        return tool
