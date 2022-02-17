import glob
import os
import time
from copy import copy

import numpy as np
from dataclasses import dataclass

from valcon import Strategy, InputData, OutputData
from valcon.scorer import Scorer
from valcon.utils import best_score, generate_file_name, get_problem_name, flatten

THIS_PATH = os.path.abspath(os.path.dirname(__file__))


class MyStragegy(Strategy):

    def solve(self, input_data: InputData) -> OutputData:
        return OutputData()


if __name__ == '__main__':
    directory = os.path.join(THIS_PATH, 'input')
    output_directory = os.path.join(THIS_PATH, 'output')

    files = glob.glob(os.path.join(directory, "*.in"))

    current_best = best_score(output_directory)

    for problem_file in files:
        problem_name = get_problem_name(problem_file)
        print(f'--- {problem_name} ---')

        problem = InputData(problem_file)

        solver = MyStragegy()
        scorer = Scorer(problem)

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
