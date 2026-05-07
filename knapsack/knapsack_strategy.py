from abc import ABC, abstractmethod

class Strategy(ABC):

    @abstractmethod
    def solve(self, instance: dict) -> dict:
        """Abstract method to be implemented"""
        pass