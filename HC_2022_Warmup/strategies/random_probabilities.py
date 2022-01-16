import os

import numpy as np

from HC_2022_Warmup.perfect_pizza import PerfectPizza
from HC_2022_Warmup.pizza_demands import PizzaDemands
from HC_2022_Warmup.strategies.default import Default
from valcon import Strategy

THIS_PATH = os.path.abspath(os.path.dirname(__file__))


class RandomClientProbability(Strategy):
    def __init__(self, seed, n_clients, customer_probabilities):
        super().__init__(seed)
        self.n_clients = n_clients
        self.customer_probabilities = np.array(customer_probabilities)
        if self.customer_probabilities.min() < 0:
            raise ValueError("Probabilities must be non-negative")
        if self.customer_probabilities.sum() != 1:
            self.customer_probabilities /= self.customer_probabilities.sum()

    def solve(self, input_data: PizzaDemands) -> PerfectPizza:
        random_customer_ids = self.rng.choice(
            len(self.customer_probabilities),
            size=self.n_clients,
            replace=False,
            p=self.customer_probabilities,
        )
        return Default(customer_ids=random_customer_ids).solve(input_data)
