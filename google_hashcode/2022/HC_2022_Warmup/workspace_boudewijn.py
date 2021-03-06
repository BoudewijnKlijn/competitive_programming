import os
import time

import numpy as np
from typing import List, Tuple, Dict, Any, Optional, Iterable

import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

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


class HillClimber(Strategy):
    def __init__(self, scorer, score_to_beat, customer_ids=Iterable[int], add=True, remove=True, replace=True):
        super().__init__(repeatable=False)
        self.customer_ids = customer_ids
        self.add = add
        self.remove = remove
        self.replace = replace
        self.scorer = scorer
        self.score_to_beat = score_to_beat

    def solve(self, input_data: PizzaDemands) -> PerfectPizza:
        excluded_customer_ids = [customer_id for customer_id in range(len(input_data.customers))
                                 if customer_id not in self.customer_ids]

        # add customers
        if self.add:
            for customer_id in excluded_customer_ids:
                customer_ids_test = list(self.customer_ids) + [customer_id]  # transform to list otherwise numpy will add customer id to all values
                solution = Default(customer_ids=customer_ids_test).solve(input_data)
                score = self.scorer.calculate(solution)
                if score > self.score_to_beat:
                    self.best_score = score
                    self.best_output = solution
                    return solution

            print("No better solution found")
            return solution


if __name__ == '__main__':
    # problem_file = 'a_an_example.in.txt'
    # problem_file = 'b_basic.in.txt'
    # problem_file = 'c_coarse.in.txt'
    problem_file = 'd_difficult.in.txt'
    # problem_file = 'e_elaborate.in.txt'
    problem = problem_file[0]
    directory = os.path.join(THIS_PATH, 'input')
    output_directory = os.path.join(THIS_PATH, 'output')
    demands = PizzaDemands(os.path.join(directory, problem_file))
    scorer = PerfectPizzaScore(demands)

    initial_strategy = RandomClientProbability(
        seed=2479,
        n_clients=700,
        customer_probabilities=[
            1 / sum([
                 sum([np.sqrt(demands.count_likes[dislike]) for dislike in customer.dislikes]),
                 sum([np.sqrt(demands.count_dislikes[like]) for like in customer.likes]),
            ])
            for customer in demands.customers],
        label='sqrt likes dislikes',
    )
    initial_solution = initial_strategy.solve(demands)
    initial_score = scorer.calculate(initial_solution)
    print(f'Initial score: {initial_score}')

    strategy = HillClimber(scorer=scorer, score_to_beat=initial_score, customer_ids=initial_strategy.customer_ids)
    solution = strategy.solve(demands)
    score = scorer.calculate(solution)
    print(f'Score: {score}')

    current_best = best_score(output_directory)
    if current_best[problem] < strategy.best_score:
        out_file = f'{problem}-{strategy.best_score:06d}-{strategy.name}.txt'
        print(f'Writing {out_file}')
        strategy.best_output.save(os.path.join(output_directory, out_file))

    # make_plot = True
    # n_repetitions = 100
    # n_clients = len(demands.customers) // 2
    #
    # strategies = []
    # # n_clients_iter = [700]
    # n_clients_iter = range(1, len(demands.customers) // 2, 100) # range(600, 1000, 50) for E?? # range(1, len(demands.customers) // 2, 100)  # for D
    # # n_clients_iter = range(1000, len(demands.customers), 100)  # for E
    # for n_clients in n_clients_iter:
    #     n_clients = min(n_clients, len(demands.customers))
    #     strategies += [
    #         # Default(customer_ids=range(n_clients)),
    #         # TryAll(),
    #
    #         # Does NOT discriminate between ingredients
    #         # RandomClients(seed=1, n_clients=n_clients),  # Note: may contain duplicate clients
    #         # RandomClientProbability(
    #         #     seed=1,
    #         #     n_clients=n_clients,
    #         #     customer_probabilities=[1. for customer in demands.customers],  # equal probability
    #         #     label='equal',
    #         # ),
    #         # RandomClientProbability(
    #         #     seed=1,
    #         #     n_clients=n_clients,
    #         #     customer_probabilities=[1 / (1 + len(customer.dislikes)) for customer in demands.customers],
    #         #     label='dislikes',
    #         # ),
    #         # RandomClientProbability(
    #         #     seed=1,
    #         #     n_clients=n_clients,
    #         #     customer_probabilities=[1 / (1 + len(customer.likes)) for customer in demands.customers],
    #         #     label='likes',
    #         # ),
    #         # RandomClientProbability(
    #         #     seed=1,
    #         #     n_clients=n_clients,
    #         #     customer_probabilities=[1 / (len(customer.likes) + len(customer.dislikes))
    #         #                             for customer in demands.customers],
    #         #     label='likes_and_dislikes',
    #         # ),
    #
    #         # DOES discriminate between ingredients
    #         # RandomClientProbability(
    #         #     seed=1,
    #         #     n_clients=n_clients,
    #         #     customer_probabilities=[
    #         #         1 / (1 + sum([demands.count_likes[dislike] for dislike in customer.dislikes]))
    #         #         for customer in demands.customers],
    #         #     label='normal',
    #         # ),
    #         # RandomClientProbability(
    #         #     seed=1,
    #         #     n_clients=n_clients,
    #         #     customer_probabilities=[1 / (1 + sum([np.sqrt(demands.count_likes[dislike]) for dislike in customer.dislikes]))
    #         #                             for customer in demands.customers],
    #         #     label='sqrt',
    #         # ),
    #         # RandomClientProbability(
    #         #     seed=1,
    #         #     n_clients=n_clients,
    #         #     customer_probabilities=[
    #         #         1 / sum([
    #         #              sum([np.sqrt(demands.count_likes[dislike]) for dislike in customer.dislikes]),
    #         #              sum([np.sqrt(demands.count_dislikes[like]) for like in customer.likes]),
    #         #         ])
    #         #         for customer in demands.customers],
    #         #     label='sqrt likes dislikes',
    #         # ),
    #     ]
    #
    # scores_df = pd.DataFrame()
    # for strategy in strategies:
    #     start = time.perf_counter()
    #
    #     if strategy.repeatable:
    #         strategy = scorer.repeat_solve(strategy, n_repetitions=n_repetitions)
    #     else:
    #         strategy = scorer.repeat_solve(strategy, n_repetitions=1)
    #
    #     duration = time.perf_counter() - start
    #     if make_plot:
    #         try:
    #             scores_df = scores_df.append(pd.DataFrame({
    #                 'score': strategy.best_score,
    #                 'strategy': strategy.name.split('(')[0] + ' ' + strategy.label,
    #                 'n_clients': strategy.n_clients,
    #             }, index=[0]), ignore_index=True)
    #         except Exception as e:
    #             print(e)
    #             pass
    #     print(f'{problem.upper()} - score: {strategy.best_score:6d} ({duration:3.0f}s) - {strategy.name}')
    #
    #     current_best = best_score(output_directory)
    #
    #     if current_best[problem] < strategy.best_score:
    #         out_file = f'{problem}-{strategy.best_score:06d}-{strategy.name}.txt'
    #         print(f'Writing {out_file}')
    #         strategy.best_output.save(os.path.join(output_directory, out_file))
    #
    # if make_plot:
    #     sns.lineplot(data=scores_df, x="n_clients", y="score", hue="strategy")
    #     plt.show()
