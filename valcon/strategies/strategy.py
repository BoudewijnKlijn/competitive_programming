from abc import ABC, abstractmethod
from random import Random

from valcon import OutputData, InputData


class Strategy(ABC):
    """ don't forget to call super().__init__()"""

    def __init__(self, seed=27):
        self.random = Random(seed)

    @abstractmethod
    def solve(self, input_data: InputData) -> OutputData:
        pass
