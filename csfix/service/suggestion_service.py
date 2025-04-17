from csfix.llm.llm_client import LLMClient


class SuggestionService:
    def __init__(self, llm_client: LLMClient):
        self._llm_client = llm_client
