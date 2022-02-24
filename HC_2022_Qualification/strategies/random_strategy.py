import random

from .base_strategy import BaseStrategy
from ..problem_data import ProblemData
from ..solution import Solution


class RandomStrategy(BaseStrategy):

    def __init__(self, seed: int = None):
        if seed:
            self.seed = seed
        else:
            self.seed = random.randint(0, 999_999_999)
        super().__init__(seed)

    def solve(self, input_data: ProblemData) -> Solution:
        pass
