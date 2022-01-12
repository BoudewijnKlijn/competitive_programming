import os
import time

from HC_2022_Warmup.perfect_pizza_score import PerfectPizzaScore
from HC_2022_Warmup.pizza_demands import PizzaDemands
from HC_2022_Warmup.strategies.try_all import TryAll

THIS_PATH = os.path.abspath(os.path.dirname(__file__))


if __name__ == '__main__':
    problem_file = 'c_coarse.in.txt'
    directory = os.path.join(THIS_PATH, 'input')
    output_directory = os.path.join(THIS_PATH, 'output')
    demands = PizzaDemands(os.path.join(directory, problem_file))

    strategy = TryAll(seed=27)
    start = time.perf_counter()
    solution = strategy.solve(demands)
    duration = time.perf_counter() - start

    scorer = PerfectPizzaScore(demands)
    score = scorer.calculate(solution)

    print(f'{problem_file} Score: {score} ({duration:0.0f}s)')

    out_file = f'{os.path.basename(problem_file)[0]}-{score:06d}-boudewijn.txt'
    print(f'Writing {out_file}')

    solution.save(os.path.join(output_directory, out_file))
