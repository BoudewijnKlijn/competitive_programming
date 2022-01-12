from HC_2022_Warmup.perfect_pizza import PerfectPizza
from HC_2022_Warmup.pizza_demands import PizzaDemands
from valcon import Strategy, InputData, OutputData
from valcon.utils import flatten


class RandomIngredients(Strategy):
    def __init__(self, seed=None, nr_ingredients=5):
        super().__init__(seed)
        self.nr_ingredients = nr_ingredients

    def solve(self, input_data: PizzaDemands) -> PerfectPizza:
        ingredients = set(flatten(customer.likes for customer in input_data.customers))
        chosen = self.random.sample(ingredients, self.nr_ingredients)
        return PerfectPizza(chosen)
