import os
import time

from HC_2022_Warmup.perfect_pizza_score import PerfectPizzaScore
from HC_2022_Warmup.pizza_demands import PizzaDemands
from HC_2022_Warmup.strategies import RandomIngredients

THIS_PATH = os.path.abspath(os.path.dirname(__file__))

if __name__ == '__main__':
    problem_file = 'a_an_example.in.txt'
    directory = os.path.join(THIS_PATH, 'input')
    demands = PizzaDemands(os.path.join(directory, problem_file))

    strategy = RandomIngredients(seed=27, nr_ingredients=3)
    start = time.perf_counter()
    solution = strategy.solve(demands)
    duration = time.perf_counter() - start

    scorer = PerfectPizzaScore(demands)
    score = scorer.calculate(solution)

    print(f'{problem_file} Score: {score} ({duration:0.0f}s)')
