from abc import abstractmethod

from ..problem_data import ProblemData
from ..solution import Solution
from valcon import Strategy


class BaseStrategy(Strategy):

    def __init__(self, seed: int = None):
        super().__init__(seed)

    @abstractmethod
    def solve(self, input_data: ProblemData) -> Solution:
        pass
