import glob
import os

from HC_2018_Qualification.city_data import CityData

# from HC_2019_Qualification.precalc_transition_scores import best_score
from HC_2018_Qualification.strategies.baseline_solver import BaseLineStrategy

THIS_PATH = os.path.abspath(os.path.dirname(__file__))

if __name__ == '__main__':
    directory = os.path.join(THIS_PATH, 'input')
    output_directory = os.path.join(THIS_PATH, 'output')

    files = glob.glob(os.path.join(directory, "*.in"))

    # current_best = best_score(output_directory)

    files = ['./input/a_example.in']
    for problem_file in files:
        problem_file = os.path.abspath(problem_file)
        problem = os.path.basename(problem_file)[0]
        city_data = CityData(problem_file)

        strategy = BaseLineStrategy()
        output_data = strategy.solve(city_data)
        print(output_data)