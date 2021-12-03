from HC_2019_Qualification.Pictures import Pictures
from HC_2019_Qualification.slides import Slides
from HC_2019_Qualification.strategies.baseline_solver import BaseLineStrategy
from valcon.strategy import Strategy


class SortByNTagsStrategy(Strategy):
    def solve(self, input_data: Pictures) -> Slides:
        input_data.pictures = sorted(input_data.pictures, key=lambda x: x.number_of_tags, reverse=True)

        return BaseLineStrategy().solve(input_data)
