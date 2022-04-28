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
        print(f'{problem_file}')

        load_start = time.perf_counter()
        problem = ProblemData(problem_file)
        load_end = time.perf_counter()
        print(f'Load time: {load_end-load_start:.2f}s')

        solve_start = time.perf_counter()
        solver = strategy
        solution = solver.solve(problem)
        solve_end = time.perf_counter()
        print(f'Solve time: {solve_end - solve_start:.2f}s')

        score_start = time.perf_counter()
        scorer = Score(problem, verbose=True)
        score = scorer.calculate(solution)
        score_end = time.perf_counter()
        print(f'Score time: {score_end - score_start:.2f}s')

        duration = score_end - load_start
        print(f'Score: {score} ({duration:0.2f}s)')

        if score > current_best[problem_name]:
            out_file = generate_file_name(problem_file, score, solver)
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

