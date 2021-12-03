import os
import time

from HC_2019_Qualification.Pictures import Pictures
from HC_2019_Qualification.slide import Slide
from HC_2019_Qualification.slides import Slides
from HC_2019_Qualification.strategies.baseline_solver import BaseLineStrategy
from HC_2019_Qualification.scorer_2019_q import Scorer2019Q
from strategies.brute_force_strategy import BruteForceSlidesStrategy
from valcon import OutputData
from valcon import Strategy

from tqdm import tqdm
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


class IslandStrategy(Strategy):
    """ and island is either a single picture or a set of pictures that have a transition with a score >= 1"""

    def __init__(self, seed=None, iterations=10):
        self.iterations = iterations
        self.rng = random.Random()
        self.rng.seed(seed)

    def get_islands(self, slides: Slides) -> [Slides]:
        islands = []

        island = [slides.slides[0]]
        for slide in slides.slides[1:]:

            score = Scorer2019Q.calculate_transition(island[-1], slide)
            if score > 0:
                island.append(slide)
            else:
                islands.append(Slides(island))
                island = [slide]

        return islands

    def solve(self, input_data: Pictures) -> OutputData:
        self.rng.shuffle(input_data.pictures)

        solution = BaseLineStrategy().solve(input_data)

        for _ in tqdm(range(self.iterations)):
            islands = self.get_islands(solution)
            self.rng.shuffle(islands)
            solution = Slides(islands)

        return solution


if __name__ == '__main__':
    directory = os.path.join(THIS_PATH, 'HC_2019_Qualification', 'input')
    pictures = Pictures(os.path.join(directory, 'b_lovely_landscapes.txt'))

    strategy = IslandStrategy(seed=1, iterations=100)
    start = time.perf_counter()
    solution = strategy.solve(pictures)
    duration = time.perf_counter() - start

    scorer = Scorer2019Q(pictures)
    score = scorer.calculate(solution)

    print(f'Score: {score} ({duration:0.0f}s)')
    # print(f'Slides: {solution}')

    pass
