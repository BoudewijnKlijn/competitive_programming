from random import Random

from HC_2019_Qualification.Pictures import Pictures
from HC_2019_Qualification.slides import Slides
from HC_2019_Qualification.strategies.baseline_solver import BaseLineStrategy
from valcon.strategies.strategy import Strategy


class RandomThenSortByNTagsStrategy(Strategy):
    def __init__(self, seed: int):
        self.seed = seed

    def solve(self, input_data: Pictures) -> Slides:
        rng = Random(self.seed)
        rng.shuffle(input_data.pictures)

        input_data.pictures = sorted(input_data.pictures, key=lambda x: x.number_of_tags, reverse=True)

        return BaseLineStrategy().solve(input_data)
