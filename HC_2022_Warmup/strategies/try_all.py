from itertools import product

from HC_2022_Warmup.perfect_pizza import PerfectPizza
from HC_2022_Warmup.perfect_pizza_score import PerfectPizzaScore
from HC_2022_Warmup.pizza_demands import PizzaDemands
from valcon import Strategy
from valcon.utils import flatten


class TryAll(Strategy):
    def __init__(self, seed=None):
        super().__init__(seed)

    def solve(self, input_data: PizzaDemands) -> PerfectPizza:
        ingredient_list = list(set(flatten(customer.likes for customer in input_data.customers)))
        options = [True, False]
        best_pizza = None
        best_score = None
        scorer = PerfectPizzaScore(input_data)

        for i, include_pizzas in enumerate(product(options, repeat=len(ingredient_list))):
            if i % 100 == 0:
                print(i, best_score)
            candidate_ingredients = list()
            for ingredient, include_pizza in zip(ingredient_list, include_pizzas):
                if include_pizza:
                    candidate_ingredients.append(ingredient)
            candidate_perfect_pizza = PerfectPizza(candidate_ingredients)
            score = scorer.calculate(candidate_perfect_pizza)

            if best_score is None or score > best_score:
                best_pizza = candidate_perfect_pizza
                best_score = score

        return best_pizza
