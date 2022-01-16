import os

from HC_2022_Warmup.perfect_pizza import PerfectPizza
from HC_2022_Warmup.pizza_demands import PizzaDemands
from valcon import OutputData, InputData
from valcon.scorer import Scorer
from valcon.utils import best_score
from valcon import Strategy


THIS_PATH = os.path.abspath(os.path.dirname(__file__))
OUTPUT_DIRECTORY = os.path.join(THIS_PATH, 'output')


class PerfectPizzaScore(Scorer):
    def __init__(self, input_data: PizzaDemands):
        self.pizza_demands = input_data

    def calculate(self, output_data: PerfectPizza) -> int:
        score = 0
        for customer in self.pizza_demands.customers:
            if customer.will_order(output_data):
                score += 1
        return score

    def repeat_solve(self, strategy: Strategy, n_repetitions: int) -> Strategy:
        for seed in range(n_repetitions):
            strategy.change_seed(seed)
            solution = strategy.solve(self.pizza_demands)
            score = self.calculate(solution)
            if strategy.best_score is None or score > strategy.best_score:
                strategy.best_seed = seed
                strategy.best_score = score
                strategy.best_output = solution
                if solution is None:
                    print(seed, 'None')
        return strategy
