import os

from qualifier.calculate_score import calculate_score
from qualifier.input_data import InputData
from qualifier.output_data import OutputData
from qualifier.strategy import Strategy
from qualifier.random_strategy import RandomStrategy

THIS_PATH = os.path.realpath(__file__)


class MyStrategy(Strategy):

    def solve(self, input):
        return OutputData(input.data)


if __name__ == '__main__':

    directory = os.path.join(THIS_PATH, '../inputs')
    for file_name in os.listdir(directory):
        input_data = InputData(os.path.join(directory, file_name))
        my_strategy = RandomStrategy(strategy=MyStrategy)
        output = my_strategy.solve(input_data)

        score = calculate_score(output)

        case_name = os.path.splitext(file_name)[0]

        file_name = f'marco_{score}_{case_name}.out'
        output.save(file_name)
