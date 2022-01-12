import os
import time

import numpy as np
from typing import List, Tuple, Dict, Any, Optional
from HC_2022_Warmup.perfect_pizza import PerfectPizza
from HC_2022_Warmup.perfect_pizza_score import PerfectPizzaScore
from HC_2022_Warmup.pizza_demands import PizzaDemands
from HC_2022_Warmup.strategies.random_ingredients import RandomIngredients
from HC_2022_Warmup.strategies.try_all import TryAll
from HC_2022_Warmup.strategies.random_probabilities import RandomProbability
from valcon import Strategy
from scipy.special import softmax
THIS_PATH = os.path.abspath(os.path.dirname(__file__))


if __name__ == '__main__':
    # problem_file = 'a_an_example.in.txt'
    # problem_file = 'b_basic.in.txt'
    # problem_file = 'c_coarse.in.txt'
    # problem_file = 'd_difficult.in.txt'
    problem_file = 'e_elaborate.in.txt'
    directory = os.path.join(THIS_PATH, 'input')
    output_directory = os.path.join(THIS_PATH, 'output')
    demands = PizzaDemands(os.path.join(directory, problem_file))

    # strategy = TryAll(seed=27)
    ingredient_probabilities = {ingredient: 1 for ingredient in demands.unique_likes}  # equal weight == 1
    ingredient_probabilities = {ingredient: 0 for ingredient in demands.unique_likes}  # equal weight == 0
    change_ingredient = list(demands.unique_likes)[0]
    print(change_ingredient)
    ingredient_probabilities[change_ingredient] = 1  # one ingredient with 100% probability
    # print(ingredient_probabilities)

    strategy = RandomProbability(ingredient_probabilities=ingredient_probabilities, seed=27)
    start = time.perf_counter()
    solution = strategy.solve(demands)
    duration = time.perf_counter() - start

    scorer = PerfectPizzaScore(demands)
    score = scorer.calculate(solution)

    print(f'{problem_file} Score: {score} ({duration:0.0f}s)')

    out_file = f'{os.path.basename(problem_file)[0]}-{score:06d}-boudewijn.txt'
    print(f'Writing {out_file}')

    solution.save(os.path.join(output_directory, out_file))
