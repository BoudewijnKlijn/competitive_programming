r"""
Run as module using the -m option.

example:
C:\Users\marco\repos\Valcon_Hash_Code_2022>python -m HC_2022_Qualification.runner_marco

"""

import glob
import os
import time
from copy import copy

import numpy as np
from dataclasses import dataclass

from .strategies.random_strategy import RandomStrategy
from .problem_data import ProblemData
from .score import Score
from .solution import Solution
from .strategies.base_strategy import BaseStrategy
from valcon.utils import best_score, generate_file_name, get_problem_name, flatten

THIS_PATH = os.path.abspath(os.path.dirname(__file__))

if __name__ == '__main__':
    directory = os.path.join(THIS_PATH, 'input')
    output_directory = os.path.join(THIS_PATH, 'output')

    files = glob.glob(os.path.join(directory, "*.txt"))

    current_best = best_score(output_directory)

    problems_to_solve = [
        'a',
        'b',
        'c',
        'd',
        'e',
    ]

    while True:

        for problem_file in files:
            problem_name = get_problem_name(problem_file)

            if problem_name not in problems_to_solve:
                continue

            print(f'--- {problem_name} ---')

            problem = ProblemData(problem_file)

            solver = RandomStrategy()
            scorer = Score(problem)

            start = time.perf_counter()
            solution = solver.solve(problem)
            duration = time.perf_counter() - start

            score = scorer.calculate(solution)

            print(f'{problem_file} Score: {score} ({duration:0.0f}s)')

            out_file = generate_file_name(problem_file, score, solver)

            if score > current_best[problem_name]:
                print(f'Writing {out_file}')
                solution.save(os.path.join(output_directory, out_file))
            else:
                print(f'No improvement for {problem_name}')

            print('\n')

        print(best_score(output_directory))
