import glob
import os
import numpy as np

from HC_2018_Qualification.car_schedules import CarSchedules
from HC_2018_Qualification.city_data import CityData

# from HC_2019_Qualification.precalc_transition_scores import best_score
from valcon import Strategy, InputData, OutputData

THIS_PATH = os.path.abspath(os.path.dirname(__file__))

#
# class Randomnessie(Strategy):
#
#     def solve(self, input_data: CityData) -> CarSchedules:
#         P = len(input_data.vehicles)
#         split_points = np.random.choice(P - 2, I - 1, replace=False) + 1
#         split_points.sort()
#         result = np.split(data, split_points)


if __name__ == '__main__':
    directory = os.path.join(THIS_PATH, 'input')
    output_directory = os.path.join(THIS_PATH, 'output')

    files = glob.glob(os.path.join(directory, "*.in"))

    # current_best = best_score(output_directory)

    # problem_file = 'a_an_example.in.txt'
    for problem_file in files:
        problem = os.path.basename(problem_file)[0]
        city_data = CityData(problem_file)
        print(city_data)

        # demands = PizzaDemands(os.path.join(directory, problem_file))
        # scorer = PerfectPizzaScore(demands)
        # strategy = MipSolverStrategy(scorer, seed=27)
        # start = time.perf_counter()
        # solution = strategy.solve(demands)
        # duration = time.perf_counter() - start
        #
        # score = scorer.calculate(solution)
        #
        # print(f'{problem_file} Score: {score} ({duration:0.0f}s)')
        #
        # out_file = f'{os.path.basename(problem_file)[0]}-{score:06d}-{strategy.name}.txt'
        # print(f'Writing {out_file}')
        #
        # if current_best[problem] < score:
        #     solution.save(os.path.join(output_directory, out_file))

    # print(best_score(output_directory))
