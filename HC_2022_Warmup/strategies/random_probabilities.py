import os
from typing import Dict

import numpy as np
from scipy.special import softmax

from HC_2022_Warmup.perfect_pizza import PerfectPizza
from HC_2022_Warmup.pizza_demands import PizzaDemands
from valcon import Strategy

THIS_PATH = os.path.abspath(os.path.dirname(__file__))


class RandomProbability(Strategy):
    def __init__(self, ingredient_probabilities: Dict[str, float], seed=None):
        super().__init__(seed)
        self.ingredients, self.probabilities = zip(*ingredient_probabilities.items())
        if sum(self.probabilities) != 1:
            # Apply softmax to probabilities so that they sum to 1.
            self.probabilities = softmax(self.probabilities)

    def solve(self, input_data: PizzaDemands) -> PerfectPizza:
        number = self.random.randint(1, len(self.ingredients))
        chosen = np.random.choice(self.ingredients, size=number, replace=False, p=self.probabilities)
        return PerfectPizza(chosen)
