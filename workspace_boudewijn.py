import os

from HC_2019_Qualification.strategies.sort_by_n_tags import SortByNTagsStrategy
from HC_2019_Qualification.strategies.random_solver import RandomStrategy
from HC_2019_Qualification.strategies.random_into_sort import RandomThenSortByNTagsStrategy
from HC_2019_Qualification.strategies.random_sort_flip import RandomSortFlipStrategy
from HC_2019_Qualification.input_data_2019_q import Pictures
from HC_2019_Qualification.scorer_2019_q import Scorer2019Q

THIS_PATH = os.path.abspath(os.path.dirname(__file__))

if __name__ == '__main__':
    directory = os.path.join(THIS_PATH, 'HC_2019_Qualification', 'input')
    input_data = Pictures(os.path.join(directory, 'b_lovely_landscapes.txt'))

    # strategy = SortByNTagsStrategy()
    # strategy = RandomStrategy(None)
    # strategy = RandomThenSortByNTagsStrategy(None)
    strategy = RandomSortFlipStrategy(0)
    solution = strategy.solve(input_data)

    scorer = Scorer2019Q(input_data)
    score = scorer.calculate(solution)

    print(f'Score: {score}')

    pass
