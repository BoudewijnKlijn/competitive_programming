import os
import time
import glob

from HC_2019_Qualification.workspace_marco import flatten
from HC_2022_Warmup.perfect_pizza import PerfectPizza
from HC_2022_Warmup.perfect_pizza_score import PerfectPizzaScore
from HC_2022_Warmup.pizza_demands import PizzaDemands
from HC_2022_Warmup.strategies import RandomIngredients
from valcon import Strategy, InputData, OutputData

THIS_PATH = os.path.abspath(os.path.dirname(__file__))

from collections import Counter


class ScoredIngredients(Strategy):

    def solve(self, input_data: PizzaDemands) -> PerfectPizza:
        likes_counts = Counter(flatten(customer.likes for customer in input_data.customers))
        dislike_counts = Counter(flatten(customer.dislikes for customer in input_data.customers))

        ingredients = set(likes_counts.keys())

        ingredients_value = dict()
        for ingredient in ingredients:
            ingredients_value[ingredient] = likes_counts[ingredient] - dislike_counts[ingredient]

        import heapq
        best = heapq.nlargest(5, ingredients_value, key=ingredients_value.get)
        return PerfectPizza(best)


if __name__ == '__main__':
    problem_file = 'b_basic.in.txt'
    directory = os.path.join(THIS_PATH, 'input')
    output_directory = os.path.join(THIS_PATH, 'output')
    demands = PizzaDemands(os.path.join(directory, problem_file))

    files = glob.glob(os.path.join(directory, "*.txt"))

    # problem_file = 'a_an_example.in.txt'
    for problem_file in files:
        strategy = ScoredIngredients(seed=27)
        start = time.perf_counter()
        solution = strategy.solve(demands)
        duration = time.perf_counter() - start

        scorer = PerfectPizzaScore(demands)
        score = scorer.calculate(solution)

        print(f'{problem_file} Score: {score} ({duration:0.0f}s)')

        solution.save(os.path.join(output_directory, f'{problem_file[0]}-{score}-marco.txt'))
