from abc import ABC, abstractmethod
from random import Random

from numpy.random import default_rng

from valcon import OutputData, InputData


class Strategy(ABC):
    """ don't forget to call super().__init__()"""

    @property
    def name(self):
        if self.best_seed:
            return f'{type(self).__name__}({self.best_seed})'
        else:
            return f'{type(self).__name__}({self.seed})'  # TODO: remove, just to make it backward compatible

    def __init__(self, seed=0, repeatable=True, label=None):
        self.seed = seed
        self.random = Random()
        self.random.seed(seed)
        self.rng = default_rng(seed)
        self.repeatable = repeatable
        self.best_seed = None
        self.best_score = None
        self.best_output = None
        self.label = str(label)

    def change_seed(self, seed: int):
        self.seed = seed
        self.random.seed(seed)
        self.rng = default_rng(seed)

    @abstractmethod
    def solve(self, input_data: InputData) -> OutputData:
        pass
