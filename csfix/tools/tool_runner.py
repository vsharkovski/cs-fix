from abc import ABC, abstractmethod
from pathlib import Path

from csfix.model.problem import Problem


class ToolRunner(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def run(self, file: Path) -> list[Problem]:
        pass
