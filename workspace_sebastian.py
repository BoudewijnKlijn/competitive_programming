import os

from HC_2019_Qualification.strategies.SortByNPicture_solver import SortByNPicturesStrategy
from HC_2019_Qualification.input_data_2019_q import Pictures
from HC_2019_Qualification.scorer_2019_q import Scorer2019Q

THIS_PATH = os.path.abspath(os.path.dirname(__file__))

if __name__ == '__main__':
    directory = os.path.join(THIS_PATH, 'HC_2019_Qualification', 'input')
    input_data = Pictures(os.path.join(directory, 'a_example.txt'))

    strategy = SortByNPicturesStrategy()
    solution = strategy.solve(input_data)

    scorer = Scorer2019Q(input_data)
    score = scorer.calculate(solution)

    print(f'Score: {score}')

    pass
