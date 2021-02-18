from abc import ABC

from qualifier.input_data import InputData
from qualifier.output_data import OutputData
from random import Random


class Strategy(ABC):
    def __init__(self, seed=27):
        self.random = Random()
        self.random.seed(seed)

    def solve(self, input: InputData) -> OutputData:
        return OutputData()
