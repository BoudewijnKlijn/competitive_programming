import random

from .base_strategy import BaseStrategy
from .baseline_strategy import BaselineStrategy
from ..problem_data import ProblemData
from ..solution import Solution


class RandomStrategy(BaseStrategy):

    def __init__(self, seed: int = None):
        """
        Initializes a RandomStrategy which assign random contributors to a project

        Args:
            seed (int): Seed for random generator
        """
        if seed:
            self.seed = seed
        else:
            self.seed = random.randint(0, 999_999_999)
        super().__init__(seed)

    def solve(self, input_data: ProblemData) -> Solution:
        random.shuffle(input_data.contributors)

        baseline_strategy = BaselineStrategy()

        return baseline_strategy.solve(input_data)
