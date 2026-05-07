from abc import ABC, abstractmethod
import numpy as np

class Strategy(ABC):

    @abstractmethod
    def solve(self, instance: np.ndarray) -> dict:
        """Abstract method to be implemented"""
        pass
