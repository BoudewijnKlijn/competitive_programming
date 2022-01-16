from abc import ABC, abstractmethod
from random import Random

from numpy.random import default_rng

from valcon import OutputData, InputData


class Strategy(ABC):
    """ don't forget to call super().__init__()"""

    @property
    def name(self):
        return f'{type(self).__name__}({self.seed})'

    def __init__(self, seed=None):
        self.seed = seed
        self.random = Random()
        self.random.seed(seed)
        self.rng = default_rng(seed)

    def change_seed(self, seed=None):
        self.seed = seed if seed is not None else self.seed + 1
        self.random.seed(seed)
        self.rng = default_rng(seed)

    @abstractmethod
    def solve(self, input_data: InputData) -> OutputData:
        pass
