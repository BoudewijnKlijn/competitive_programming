import os
import time

import numpy as np
from typing import List, Tuple, Dict, Any, Optional
from HC_2022_Warmup.perfect_pizza import PerfectPizza
from HC_2022_Warmup.perfect_pizza_score import PerfectPizzaScore
from HC_2022_Warmup.pizza_demands import PizzaDemands
from HC_2022_Warmup.strategies.random_ingredients import RandomIngredients
from HC_2022_Warmup.strategies.try_all import TryAll
from HC_2022_Warmup.strategies.default import Default
from HC_2022_Warmup.strategies.random_clients import RandomClients
from HC_2022_Warmup.strategies.random_probabilities import RandomClientProbability
from valcon import Strategy

from valcon.utils import best_score

THIS_PATH = os.path.abspath(os.path.dirname(__file__))


if __name__ == '__main__':
    # problem_file = 'a_an_example.in.txt'
    # problem_file = 'b_basic.in.txt'
    # problem_file = 'c_coarse.in.txt'
    # problem_file = 'd_difficult.in.txt'
    problem_file = 'e_elaborate.in.txt'
    problem = problem_file[0]
    directory = os.path.join(THIS_PATH, 'input')
    output_directory = os.path.join(THIS_PATH, 'output')
    demands = PizzaDemands(os.path.join(directory, problem_file))
    scorer = PerfectPizzaScore(demands)

    n_repetitions = 100
    n_clients = 3000
    strategies = [
        Default(customer_ids=range(n_clients)),
        RandomClients(seed=1, n_clients=n_clients),
        RandomClientProbability(
            seed=1,
            n_clients=n_clients,
            customer_probabilities=[1 / (1 + len(customer.dislikes)) for customer in demands.customers]
        ),
        RandomClientProbability(
            seed=1,
            n_clients=n_clients,
            customer_probabilities=[1 / (len(customer.likes) + len(customer.dislikes))
                                    for customer in demands.customers]
        ),

        TryAll(),
    ]

    for strategy in strategies:
        start = time.perf_counter()

        if strategy.repeatable:
            strategy = scorer.repeat_solve(strategy, n_repetitions=n_repetitions)
        else:
            strategy = scorer.repeat_solve(strategy, n_repetitions=1)

        duration = time.perf_counter() - start
        print(f'{problem.upper()} - score: {strategy.best_score:6d} ({duration:3.0f}s) - {strategy.name}')

        current_best = best_score(output_directory)

        if current_best[problem] < strategy.best_score:
            out_file = f'{problem}-{strategy.best_score:06d}-{strategy.name}.txt'
            print(f'Writing {out_file}')
            strategy.best_output.save(os.path.join(output_directory, out_file))
