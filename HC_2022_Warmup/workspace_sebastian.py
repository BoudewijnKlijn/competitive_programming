import glob
import os
import time

from HC_2022_Warmup.perfect_pizza_score import PerfectPizzaScore
from HC_2022_Warmup.pizza_demands import PizzaDemands
from HC_2022_Warmup.strategies.valuable_ingredients import ValuableIngredients

THIS_PATH = os.path.abspath(os.path.dirname(__file__))

if __name__ == '__main__':
    directory = os.path.join(THIS_PATH, 'input')
    output_directory = os.path.join(THIS_PATH, 'output')

    files = glob.glob(os.path.join(directory, "*.txt"))
    files = sorted(files)
    # problem_file = 'a_an_example.in.txt'
    # Forward selection
    for problem_file in files:
        print(f"Trying to solve file (FORWARD): {problem_file}")
        demands = PizzaDemands(os.path.join(directory, problem_file))

        scorer = PerfectPizzaScore(demands)
        strategy = ValuableIngredients(scorer, seed=27)
        start = time.perf_counter()
        solution = strategy.solve(demands)
        duration = time.perf_counter() - start

        score = scorer.calculate(solution)

        print(f'{problem_file} Score: {score} ({duration:0.0f}s)')
        print("----------------------")

        out_file = f'{os.path.basename(problem_file)[0]}-{score:06d}-sebastian.txt'
        print(f'Writing {out_file}')

        solution.save(os.path.join(output_directory, out_file))

    print("----------------------")
    print("----------------------")
    print()

    """
    for problem_file in files:
        print(f"Trying to solve file (BACKWARD): {problem_file}")
        demands = PizzaDemands(os.path.join(directory, problem_file))

        scorer = PerfectPizzaScore(demands)
        strategy = ValuableIngredients(scorer, forward_selection=False, seed=27)
        start = time.perf_counter()
        solution = strategy.solve(demands)
        duration = time.perf_counter() - start

        score = scorer.calculate(solution)

        print(f'{problem_file} Score: {score} ({duration:0.0f}s)')
        print("----------------------")
    """