from HC_2022_Warmup.perfect_pizza import PerfectPizza
from HC_2022_Warmup.pizza_demands import PizzaDemands
from valcon import Strategy
from valcon.utils import flatten


class RandomIngredients(Strategy):
    def __init__(self, seed=None):
        super().__init__(seed)

    def solve(self, input_data: PizzaDemands) -> PerfectPizza:
        ingredients = set(flatten(customer.likes for customer in input_data.customers))
        number = self.random.randint(1, len(ingredients))
        chosen = self.random.sample(ingredients, number)
        return PerfectPizza(chosen)


class RandomSetIngredients(Strategy):
    def __init__(self, nr_of_ingredients: int, seed=None):
        super().__init__(seed)
        self.nr_of_ingredients = nr_of_ingredients

    def solve(self, input_data: PizzaDemands) -> PerfectPizza:
        ingredients = set(flatten(customer.likes for customer in input_data.customers))

        chosen = self.random.sample(ingredients,
                                    int(self.nr_of_ingredients))  # int is a hack see if bayesian can do ints instead
        return PerfectPizza(chosen)
