import os

from qualifier.calculate_score import calculate_score
from qualifier.input_data import InputData
from qualifier.output_data import OutputData
from qualifier.schedule import Schedule
from qualifier.strategy import Strategy
from qualifier.util import save_output


import math

def sort_streets_on_relevance(input):
    """
    """
    route_lenghts = []
    for car in input.cars:
        route_lenghts.append(len(car.path))
    avg_route_length = sum(route_lenghts) / len(route_lenghts)


class FixedPeriods(Strategy):

    def solve(self, input):
        schedules = []
        for intersection in input.intersections:
            trafic_lights = []
            for street in intersection.incoming_streets:
                trafic_lights.append((street.name, 1))
            schedule = Schedule(intersection.index, trafic_lights)
            schedules.append(schedule)

        return OutputData(schedules)


if __name__ == '__main__':

    directory = os.path.join('inputs')
    for file_name in os.listdir(directory):
        input_data = InputData(os.path.join(directory, file_name))

        my_strategy = FixedPeriods()

        output = my_strategy.solve(input_data)

        score = calculate_score(output)

        save_output(output, file_name, score, 'diede')
