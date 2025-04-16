from abc import ABC, abstractmethod


class LLMClient(ABC):
    @abstractmethod
    def get_completion(self, messages: list[dict[str, str]]) -> str:
        pass
