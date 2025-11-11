# provider/base.py

from abc import ABC, abstractmethod

class BaseProvider(ABC):
    @abstractmethod
    def chat(self, messages: list[dict], stream: bool = False) -> str:
        pass