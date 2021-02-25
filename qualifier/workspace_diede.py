import os

from qualifier.calculate_score import calculate_score
from qualifier.input_data import InputData
from qualifier.output_data import OutputData
from qualifier.strategy import Strategy
from qualifier.util import save_output


class MyStrategy(Strategy):

    def solve(self, input):
        return OutputData(input.data)


if __name__ == '__main__':

    directory = os.path.join('inputs')
    for file_name in os.listdir(directory):
        input_data = InputData(os.path.join(directory, file_name))

        my_strategy = MyStrategy()

        output = my_strategy.solve(input_data)

        score = calculate_score(output)

        save_output(output, file_name, score, 'diede')
