import os
from collections import defaultdict

from qualifier.calculate_score import calculate_score
from qualifier.input_data import InputData
from qualifier.output_data import OutputData
from qualifier.schedule import Schedule
from qualifier.strategy import Strategy
from qualifier.util import save_output

THIS_PATH = os.path.realpath(__file__)


class MyStrategy(Strategy):

    def solve(self, input):
        schedules = []
        all_paths = [car.path for car in input.cars]
        street_counts = defaultdict(int)
        for path in all_paths:
            for street in path:
                street_counts[street.name] += 1

        for intersection in input.intersections:
            trafic_lights = []
            min_intersection = min(street_counts[street.name] for street in intersection.incoming_streets)
            any_non_zero_weight = False
            for street in intersection.incoming_streets:
                if min_intersection == 0:
                    weight = 0
                else:
                    any_non_zero_weight = True
                    weight = round(street_counts[street.name] / min_intersection)
                trafic_lights.append((street.name, weight))
            if any_non_zero_weight:
                schedule = Schedule(intersection.index, trafic_lights)
                schedules.append(schedule)

        return OutputData(schedules)


if __name__ == '__main__':

    directory = os.path.join('inputs')
    for file_name in os.listdir(directory):
    # file_name = 'a.txt'
        input_data = InputData(os.path.join(directory, file_name))

        my_strategy = MyStrategy()

        output = my_strategy.solve(input_data)

        score = calculate_score(output)

        save_output(output, file_name, score, 'boudewijn')
