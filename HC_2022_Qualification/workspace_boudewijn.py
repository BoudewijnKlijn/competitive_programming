import glob
import os
import time

from HC_2022_Qualification.problem_data import ProblemData
from HC_2022_Qualification.score import Score
from HC_2022_Qualification.strategies.baseline_strategy_v2 import BaselineStrategy
from HC_2022_Qualification.strategies.random_strategy_v2 import RandomStrategy
from HC_2022_Qualification.strategies.valuable_projects import ValuableProjectStrategy
from valcon.utils import best_score, get_problem_name, generate_file_name

THIS_PATH = os.path.abspath(os.path.dirname(__file__))


def solve_with_strategy(strategy, files, output_dir):
    current_best = best_score(output_dir)
    print(f"Nr of files {len(files)}")
    for problem_file in files:
        problem_name = get_problem_name(problem_file)
        print(f'--- {problem_name} ---')

        problem = ProblemData(problem_file)

        solver = strategy
        solution = solver.solve(problem)
        # print(f"Solution: {solution}")
        scorer = Score(problem, verbose=False)

        start = time.perf_counter()

        duration = time.perf_counter() - start

        score = scorer.calculate(solution)

        print(f'{problem_file} Score: {score} ({duration:0.0f}s)')
        out_file = generate_file_name(problem_file, score, solver)

        if score > current_best[problem_name]:
            print(f'Writing {out_file}')
            solution.save(os.path.join(output_dir, out_file))
        else:
            print(f'No improvement for {problem_name}')

        print('\n')

    print(best_score(output_directory))


if __name__ == '__main__':
    directory = os.path.join(THIS_PATH, 'input')
    output_directory = os.path.join(THIS_PATH, 'output')

    input_files = glob.glob(os.path.join(directory, "*.txt"))
    input_files = sorted(input_files)

    # solve_with_strategy(BaselineStrategy(), input_files, output_directory)
    solve_with_strategy(RandomStrategy(), input_files, output_directory)
    #solve_with_strategy(ValuableProjectStrategy(), input_files, output_directory)

