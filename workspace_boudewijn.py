import os

from HC_2019_Qualification.strategies.sort_by_n_tags import SortByNTagsStrategy
from HC_2019_Qualification.strategies.random_solver import RandomStrategy
from HC_2019_Qualification.strategies.random_into_sort import RandomThenSortByNTagsStrategy
from HC_2019_Qualification.strategies.random_sort_flip import RandomSortFlipStrategy
from HC_2019_Qualification.strategies.baseline_solver import BaseLineStrategy
from HC_2019_Qualification.strategies.default_order import NonZeroDefaultOrderStrategy
from HC_2019_Qualification.Pictures import Pictures
from HC_2019_Qualification.scorer_2019_q import Scorer2019Q, get_non_zero_slide_transitions

THIS_PATH = os.path.abspath(os.path.dirname(__file__))

if __name__ == '__main__':
    directory = os.path.join(THIS_PATH, 'HC_2019_Qualification', 'input')
    input_data = Pictures(os.path.join(directory,
                                       # 'a_example.txt'
                                       'b_lovely_landscapes.txt'
                                       # 'c_memorable_moments.txt'
                                       # 'd_pet_pictures.txt'
                                       # 'e_shiny_selfies.txt'
                                       ))

    strategy = BaseLineStrategy()
    solution = strategy.solve(input_data)
    score_values, score_rows, score_cols = get_non_zero_slide_transitions(solution)
    ordered_solution = NonZeroDefaultOrderStrategy().order(score_values, score_rows, score_cols, solution,
                                                           start_slide_id=None)

    # # strategy = SortByNTagsStrategy()
    # # strategy = RandomStrategy(None)
    # # strategy = RandomThenSortByNTagsStrategy(None)
    # strategy = RandomSortFlipStrategy(0)
    # solution = strategy.solve(input_data)

    scorer = Scorer2019Q(input_data)
    score = scorer.calculate(ordered_solution)

    print(f'Score: {score}')

    pass
