import re
from pathlib import Path

from csfix.llm.llm_client import LLMClient
from csfix.model.problem import Problem


class SuggestionService:
    def __init__(self, llm_client: LLMClient):
        self._llm_client = llm_client

    def get_suggestion(self, file_content: str, problem: Problem) -> str:
        # Create a prompt for the LLM
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful coding assistant that provides specific, actionable "
                    "suggestions to fix code problems. Focus on the exact issue and provide "
                    "clear, concise solutions."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Please help me fix the following code issue:\n\n"
                    f"Problem: {problem.description}\n"
                    f"Location: {problem.location}\n"
                    f"Tool: {problem.tool_name}\n\n"
                    f"Here's the file content:\n```python\n{file_content}\n```\n\n"
                    "Please provide a specific suggestion on how to fix this issue. "
                    "Include the exact code changes needed."
                ),
            },
        ]

        # Get suggestion from LLM
        suggestion = self._llm_client.get_completion(messages)
        return suggestion

    def get_and_apply_fix(self, file_path: Path, problem: Problem) -> tuple[bool, str]:
        """Get suggestion and apply it to the file

        Returns:
            tuple: (success_flag, message)
        """
        try:
            # Read file content
            file_content = file_path.read_text()

            # Get fix suggestion
            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are a coding assistant that fixes code problems. Provide ONLY the fixed code. "
                        "Do not include any explanations, markdown formatting, or code blocks. "
                        "Return ONLY the complete fixed file content."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Fix the following code issue:\n\n"
                        f"Problem: {problem.description}\n"
                        f"Location: {problem.location}\n"
                        f"Tool: {problem.tool_name}\n\n"
                        f"Here's the file content:\n{file_content}\n\n"
                        "Return ONLY the complete fixed file content. No explanation needed."
                    ),
                },
            ]

            fixed_content = self._llm_client.get_completion(messages)

            # Clean any possible code block formatting if the LLM added it
            fixed_content = self._clean_code_blocks(fixed_content)

            # Write the fixed content back to the file
            file_path.write_text(fixed_content)

            return True, f"Fixed {problem.description} at {problem.location}"

        except Exception as e:
            return False, f"Error applying fix: {str(e)}"

    def _clean_code_blocks(self, content: str) -> str:
        """Remove markdown code blocks if present"""
        # Remove ```python and ``` if present
        content = re.sub(r"^```python\s*\n", "", content)
        content = re.sub(r"\n```\s*$", "", content)
        return content
