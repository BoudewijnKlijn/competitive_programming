import os
import glob
import time

from HC_2022_Warmup.perfect_pizza_score import PerfectPizzaScore
from HC_2022_Warmup.pizza_demands import PizzaDemands
from HC_2022_Warmup.strategies import RandomIngredients
from HC_2022_Warmup.strategies.valuable_ingredients import ValuableIngredients

THIS_PATH = os.path.abspath(os.path.dirname(__file__))

if __name__ == '__main__':
    directory = os.path.join(THIS_PATH, 'input')
    files = glob.glob(os.path.join(directory, "*.txt"))
    
    #problem_file = 'a_an_example.in.txt'
    for problem_file in files:
        print(f"Trying to solve file: {problem_file}")
        demands = PizzaDemands(os.path.join(directory, problem_file))

        scorer = PerfectPizzaScore(demands)
        strategy = ValuableIngredients(scorer,  seed=27, nr_ingredients=3)
        start = time.perf_counter()
        solution = strategy.solve(demands)
        duration = time.perf_counter() - start

        score = scorer.calculate(solution)

        print(f'{problem_file} Score: {score} ({duration:0.0f}s)')
        print("----------------------")
