import glob
import os

from HC_2018_Qualification.city_data import CityData
# from HC_2019_Qualification.precalc_transition_scores import best_score
from HC_2018_Qualification.ride_scorer import RideScore
from HC_2018_Qualification.strategies.baseline_solver import BaseLineStrategy
from HC_2018_Qualification.strategies.random_solver import RandomSolver

THIS_PATH = os.path.abspath(os.path.dirname(__file__))


def solve_baseline(input_files):
    for problem_file in input_files:
        problem_file = os.path.abspath(problem_file)
        print(problem_file)
        problem = os.path.basename(problem_file)[0]
        input_data = CityData(problem_file)

        strategy = BaseLineStrategy()
        output_data = strategy.solve(input_data)
        # print(f"Type output_data: {type(output_data)}")
        # print(output_data)
        ride_scorer = RideScore(input_data)
        score = ride_scorer.calculate(output_data=output_data)
        print(f"Score: {score:,}")
        print('-------------------------------------------------------------------------------')


def solve_random(input_files, seed=1):
    for problem_file in input_files:
        problem_file = os.path.abspath(problem_file)
        print(problem_file)
        problem = os.path.basename(problem_file)[0]
        input_data = CityData(problem_file)

        strategy = RandomSolver(seed=seed)
        output_data = strategy.solve(input_data)
        # print(f"Type output_data: {type(output_data)}")
        # print(output_data)
        ride_scorer = RideScore(input_data)
        score = ride_scorer.calculate(output_data=output_data)
        print(f"Score: {score:,}")
        print('-------------------------------------------------------------------------------')


if __name__ == '__main__':
    directory = os.path.join(THIS_PATH, 'input')
    output_directory = os.path.join(THIS_PATH, 'output')

    files = glob.glob(os.path.join(directory, "*.in"))
    files = sorted(files)
    # current_best = best_score(output_directory)

    # files = ['./input/a_example.in']

    solve_baseline(files)
    print('-------------------------------------------------------------------------------')
    print('-------------------------------------------------------------------------------')
    solve_random(files)
