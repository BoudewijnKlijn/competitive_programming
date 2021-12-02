import os
import time

from HC_2019_Qualification.input_data_2019_q import Pictures
from HC_2019_Qualification.slide import Slide
from HC_2019_Qualification.slides import Slides
from HC_2019_Qualification.strategies.random_solver import RandomStrategy
from HC_2019_Qualification.scorer_2019_q import Scorer2019Q
from valcon import InputData, OutputData
from valcon import Strategy

from itertools import permutations

import numpy as np

import random

THIS_PATH = os.path.abspath(os.path.dirname(__file__))


class DivideAndConquerStrategy(Strategy):
    """ TODO: merge V slides
    can be made efficent by not calculating the entire score but the score change by merging slides
    """

    def __init__(self, seed=None, max_size=5):
        self.rng = random.Random()
        self.rng.seed(seed)
        self.max_size = max_size

    def partition(self, list_in, n):
        self.rng.shuffle(list_in)
        return [list_in[i::n] for i in range(n)]

    def solve_subset(self, input_data: Pictures, subset: [Slides]) -> OutputData:
        if len(subset) > self.max_size:
            subsets = self.partition(subset, self.max_size)
            subset = [self.solve_subset(input_data, slides) for slides in subsets]

        return BruteForceSlidesStrategy(Scorer2019Q(input_data)).solve(subset)

    def solve(self, input_data: Pictures) -> OutputData:
        slides = [Slides([Slide([picture])]) for picture in input_data.pictures]

        return self.solve_subset(input_data=input_data, subset=slides)


class BruteForceSlidesStrategy:
    def __init__(self, scorer: Scorer2019Q):
        self.scorer = scorer

    def solve(self, slides: [Slides]) -> Slides:
        all_orders = [Slides(permutation) for permutation in permutations(slides, len(slides))]
        all_scores = [self.scorer.calculate(solution) for solution in all_orders]

        index_max = np.argmax(all_scores)
        return all_orders[index_max]


if __name__ == '__main__':
    directory = os.path.join(THIS_PATH, 'HC_2019_Qualification', 'input')
    pictures = Pictures(os.path.join(directory, 'b_lovely_landscapes.txt'))

    strategy = DivideAndConquerStrategy(seed=824354, max_size=7)
    start = time.perf_counter()
    solution = strategy.solve(pictures)
    duration = time.perf_counter() - start

    scorer = Scorer2019Q(pictures)
    score = scorer.calculate(solution)

    print(f'Score: {score} ({duration:0.0f}s)')
    # print(f'Slides: {solution}')

    pass
