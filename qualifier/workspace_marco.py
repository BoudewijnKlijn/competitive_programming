import os

from qualifier.calculate_score import calculate_score
from qualifier.input_data import InputData
from qualifier.output_data import OutputData
from qualifier.strategy import Strategy
from qualifier.random_strategy import RandomStrategy
from qualifier.util import save_output

THIS_PATH = os.path.realpath(__file__)


class RandomPeriods(Strategy):

    def solve(self, input):
        schedule

        for intersection in input.intersections:
            nr_of_input_streets = 3

        return OutputData(input.intersections.counts(), )


if __name__ == '__main__':

    directory = os.path.join(THIS_PATH, '../inputs')
    for file_name in os.listdir(directory):
        input_data = InputData(os.path.join(directory, file_name))

        my_strategy = RandomStrategy(strategy=RandomPeriods)

        output = my_strategy.solve(input_data)

        score = calculate_score(output)

        save_output(output, file_name, score, 'marco')
