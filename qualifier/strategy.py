from abc import ABC, abstractmethod

from qualifier.input_data import InputData
from qualifier.output_data import OutputData
from random import Random


class Strategy(ABC):
    def __init__(self, seed=27) -> object:
        self.random = Random()
        self.random.seed(seed)

    @staticmethod
    def streets_with_car_at_light(input_data: InputData):
        all_streets = [car.path[:-1] for car in input_data.cars]
        return {item.name for sublist in all_streets for item in sublist}

    @abstractmethod
    def solve(self, input: InputData) -> OutputData:
        raise NotImplementedError()
