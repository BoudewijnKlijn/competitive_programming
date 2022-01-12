from HC_2022_Warmup.perfect_pizza import PerfectPizza
from HC_2022_Warmup.pizza_demands import PizzaDemands, Customer
from valcon import Strategy
from valcon.utils import flatten


class ValuableIngredients(Strategy):
    def __init__(self, scorer, seed=None):
        super().__init__(seed)
        self.scorer = scorer

    @staticmethod
    def _get_valuable_ingredients(customers: [Customer]):
        ingredients = set(flatten(customer.likes for customer in customers))
        ingredient_counts = {}
        for ingredient in ingredients:
            nr_likes = sum([1 for customer in customers if ingredient in customer.likes])
            nr_dislikes = sum([1 for customer in customers if ingredient in customer.dislikes])
            ingredient_counts[ingredient] = nr_likes - nr_dislikes

        return dict(reversed(sorted(ingredient_counts.items(), key=lambda item: item[1])))

    def solve(self, input_data: PizzaDemands) -> PerfectPizza:
        valuable_ingredients = self._get_valuable_ingredients(input_data.customers)
        print(f"Ingredient values: {valuable_ingredients}")
        highest_score = 0
        current_ingredients = []
        for ingredient, value in valuable_ingredients.items():
            # print(f"Adding the following ingredient: {ingredient} with value: {value}")
            current_ingredients.append(ingredient)
            score = self.scorer.calculate(PerfectPizza(current_ingredients))
            # print(f"Current score: {score}")

            if score <= highest_score:
                break
        print(f"Final ingredients: {current_ingredients}")
        # chosen = self.random.sample(ingredients, self.nr_ingredients)
        return PerfectPizza(current_ingredients)
