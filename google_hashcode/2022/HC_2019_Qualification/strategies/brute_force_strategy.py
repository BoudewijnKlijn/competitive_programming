from itertools import permutations

import numpy as np

from HC_2019_Qualification.scorer_2019_q import Scorer2019Q
from HC_2019_Qualification.slides import Slides


class BruteForceSlidesStrategy:
    def __init__(self, scorer: Scorer2019Q):
        self.scorer = scorer

    def solve(self, slides: [Slides]) -> Slides:
        all_orders = [Slides(permutation) for permutation in permutations(slides, len(slides))]
        all_scores = [self.scorer.calculate(solution) for solution in all_orders]

        index_max = np.argmax(all_scores)
        return all_orders[index_max]
