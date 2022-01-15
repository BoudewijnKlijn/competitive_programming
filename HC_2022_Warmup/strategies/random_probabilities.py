import os

from scipy.special import softmax

from HC_2022_Warmup.perfect_pizza import PerfectPizza
from HC_2022_Warmup.pizza_demands import PizzaDemands
from valcon import Strategy

THIS_PATH = os.path.abspath(os.path.dirname(__file__))


class RandomClientProbability(Strategy):
    def __init__(self, seed, n_clients, customer_probabilities):
        super().__init__(seed)
        self.n_clients = n_clients
        self.customer_probabilities = customer_probabilities
        if sum(self.customer_probabilities) != 1:
            # Apply softmax to probabilities so that they sum to 1.
            self.customer_probabilities = softmax(self.customer_probabilities)

    def solve(self, input_data: PizzaDemands) -> PerfectPizza:
        customer_ids = self.rng.choice(
            len(self.customer_probabilities),
            size=self.n_clients,
            replace=False,
            p=self.customer_probabilities,
        )
        ingredients = set()
        for customer_id in customer_ids:
            ingredients.update(input_data.customers[customer_id].likes)
        return PerfectPizza(list(ingredients))
