from csfix.llm.llm_client import LLMClient


class OpenAIClient(LLMClient):
    """
    Wrapper for openai.OpenAI:
    https://github.com/openai/openai-python
    """

    def __init__(self, api_key: str, model: str):
        pass

    def get_completion(self, messages: list[dict[str, str]]):
        return ""
