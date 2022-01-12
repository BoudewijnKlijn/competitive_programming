import os
import time
import glob
from random import randint

from HC_2019_Qualification.workspace_marco import flatten
from HC_2022_Warmup.perfect_pizza import PerfectPizza
from HC_2022_Warmup.perfect_pizza_score import PerfectPizzaScore
from HC_2022_Warmup.pizza_demands import PizzaDemands
from HC_2022_Warmup.strategies import RandomIngredients
from valcon import Strategy, InputData, OutputData
from valcon.utils import best_score

THIS_PATH = os.path.abspath(os.path.dirname(__file__))

from collections import Counter

import heapq


class ScoredIngredients(Strategy):
    def __init__(self, seed, scorer: PerfectPizzaScore):
        super().__init__(seed)
        self.scorer = scorer

    def solve(self, input_data: PizzaDemands) -> PerfectPizza:
        likes_counts = Counter(flatten(customer.likes for customer in input_data.customers))
        dislike_counts = Counter(flatten(customer.dislikes for customer in input_data.customers))

        ingredients = set(likes_counts.keys())

        super_score = pow(len(ingredients) + 1, 2)

        ingredients_value = dict()
        for ingredient in ingredients:
            if dislike_counts[ingredient] == 0:
                ingredients_value[ingredient] = super_score
            else:
                ingredients_value[ingredient] = pow(likes_counts[ingredient], 2) - pow(dislike_counts[ingredient], 2)

        potential = heapq.nlargest(100, ingredients_value, key=ingredients_value.get)

        # self.random.shuffle(potential)

        current = [potential.pop(0)]

        best = current.copy()
        best_score = self.scorer.calculate(PerfectPizza(best))
        while potential:
            current.append(potential.pop(0))
            if (score := self.scorer.calculate(PerfectPizza(current))) > best_score:
                best = current.copy()
                best_score = score

        return PerfectPizza(best)


if __name__ == '__main__':
    directory = os.path.join(THIS_PATH, 'input')
    output_directory = os.path.join(THIS_PATH, 'output')

    files = glob.glob(os.path.join(directory, "*.txt"))

    current_best = best_score(output_directory)

    # problem_file = 'a_an_example.in.txt'
    for problem_file in files:
        problem = os.path.basename(problem_file)[0]
        demands = PizzaDemands(os.path.join(directory, problem_file))
        scorer = PerfectPizzaScore(demands)
        strategy = ScoredIngredients(seed=27,
                                     scorer=scorer)  # RandomIngredients(randint(0, 100000))  # ScoredIngredients(seed=27, scorer=scorer)
        start = time.perf_counter()
        solution = strategy.solve(demands)
        duration = time.perf_counter() - start

        score = scorer.calculate(solution)

        print(f'{problem_file} Score: {score} ({duration:0.0f}s)')

        out_file = f'{os.path.basename(problem_file)[0]}-{score:06d}-{strategy.name}.txt'
        print(f'Writing {out_file}')

        if current_best[problem] < score:
            solution.save(os.path.join(output_directory, out_file))

    print(best_score(output_directory))
