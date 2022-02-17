from random import Random

from HC_2018_Qualification.car_schedules import CarSchedules
from HC_2018_Qualification.city_data import CityData
from HC_2018_Qualification.strategies.baseline_solver import BaseLineStrategy
from valcon.strategies.strategy import Strategy


class RandomSolver(Strategy):
    def __init__(self, seed: int):
        self.seed = seed
        super().__init__(seed)

    def solve(self, input_data: CityData) -> CarSchedules:
        rng = Random(self.seed)
        rng.shuffle(input_data.rides)

        return BaseLineStrategy().solve(input_data)

