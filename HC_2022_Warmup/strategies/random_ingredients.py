from HC_2022_Warmup.perfect_pizza import PerfectPizza
from HC_2022_Warmup.pizza_demands import PizzaDemands
from valcon import Strategy, InputData, OutputData
from valcon.utils import flatten


class RandomIngredients(Strategy):
    def __init__(self, seed=None):
        super().__init__(seed)

    def solve(self, input_data: PizzaDemands) -> PerfectPizza:
        ingredients = set(flatten(customer.likes for customer in input_data.customers))
        number = self.random.randint(1, len(ingredients))
        chosen = self.random.sample(ingredients, number)
        return PerfectPizza(chosen)
