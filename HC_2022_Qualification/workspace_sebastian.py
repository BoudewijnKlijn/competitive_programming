import glob
import os
import time

from HC_2022_Qualification.problem_data import ProblemData
from HC_2022_Qualification.score import Score
from HC_2022_Qualification.strategies.baseline_strategy import BaselineStrategy
from HC_2022_Qualification.strategies.random_strategy import RandomStrategy
from valcon.utils import best_score, get_problem_name, generate_file_name

THIS_PATH = os.path.abspath(os.path.dirname(__file__))


def solve_baseline(files, output_dir):
    current_best = best_score(output_dir)
    print(f"Nr of files {len(files)}")
    for problem_file in files:
        problem_name = get_problem_name(problem_file)
        print(f'--- {problem_name} ---')

        problem = ProblemData(problem_file)

        solver = BaselineStrategy()
        print(f"Solution: {solver.solve(problem)}")
        scorer = Score(problem)

        start = time.perf_counter()
        solution = solver.solve(problem)
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


def solve_random(files):
    current_best = best_score(output_directory)
    print(f"Nr of files {len(files)}")
    for problem_file in files:
        problem_name = get_problem_name(problem_file)
        print(f'--- {problem_name} ---')

        problem = ProblemData(problem_file)

        solver = RandomStrategy()
        print(f"Solution: {solver.solve(problem)}")
        ##break
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


if __name__ == '__main__':
    directory = os.path.join(THIS_PATH, 'input')
    output_directory = os.path.join(THIS_PATH, 'output')

    input_files = glob.glob(os.path.join(directory, "*.txt"))
    input_files = sorted(input_files)

    #solve_baseline(input_files, output_directory)
    solve_random(input_files)
