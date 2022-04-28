from typing import Iterable

from HC_2022_Warmup.perfect_pizza import PerfectPizza
from HC_2022_Warmup.pizza_demands import PizzaDemands
from valcon import Strategy


class Default(Strategy):
    def __init__(self, customer_ids: Iterable[int]):
        """Use liked ingredients of selected customers."""
        super().__init__(repeatable=False)
        self.customer_ids = customer_ids

    def solve(self, input_data: PizzaDemands) -> PerfectPizza:
        ingredients = set()
        for customer_id in self.customer_ids:
            ingredients.update(input_data.customers[customer_id].likes)
        return PerfectPizza(list(ingredients))
