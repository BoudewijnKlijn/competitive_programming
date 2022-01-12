from abc import ABC, abstractmethod, abstractproperty
from random import Random

from valcon import OutputData, InputData


class Strategy(ABC):
    """ don't forget to call super().__init__()"""

    @property
    def name(self):
        return f'{type(self).__name__}({self.seed})'

    def __init__(self, seed=27):
        self.seed = seed
        self.random = Random()
        self.random.seed(seed)

    @abstractmethod
    def solve(self, input_data: InputData) -> OutputData:
        pass
