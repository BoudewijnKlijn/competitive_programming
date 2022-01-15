from HC_2022_Warmup.perfect_pizza import PerfectPizza
from HC_2022_Warmup.pizza_demands import PizzaDemands
from valcon import Strategy


class Default(Strategy):
    def __init__(self, n_clients):
        """
        Use liked ingredients of the first n_clients customers.
        :param n_clients: number of clients, must be > 0.
        """
        super().__init__()
        assert n_clients > 0, "n_clients must be > 0."
        self.n_clients = n_clients

    def solve(self, input_data: PizzaDemands) -> PerfectPizza:
        ingredients = set()
        for customer in input_data.customers[:self.n_clients]:
            ingredients.update(customer.likes)
        return PerfectPizza(list(ingredients))
