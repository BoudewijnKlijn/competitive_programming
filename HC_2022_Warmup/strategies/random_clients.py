from HC_2022_Warmup.perfect_pizza import PerfectPizza
from HC_2022_Warmup.pizza_demands import PizzaDemands
from HC_2022_Warmup.strategies.default import Default
from valcon import Strategy


class RandomClients(Strategy):
    def __init__(self, seed, n_clients):
        """
        First shuffle customers list. Then apply default strategy which uses liked ingredients of first n_clients
        in customers list.
        :param seed: random seed
        :param n_clients: number of clients, must be > 0
        """
        super().__init__(seed)
        self.n_clients = n_clients

    def solve(self, input_data: PizzaDemands) -> PerfectPizza:
        random_customer_ids = self.rng.integers(len(input_data.customers), size=self.n_clients)
        return Default(customer_ids=random_customer_ids).solve(input_data)
