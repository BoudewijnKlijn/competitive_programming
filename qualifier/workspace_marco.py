import os

from qualifier.calculate_score import calculate_score
from qualifier.input_data import InputData
from qualifier.output_data import OutputData
from qualifier.schedule import Schedule
from qualifier.strategy import Strategy
from qualifier.util import save_output

THIS_PATH = os.path.realpath(__file__)


class FixedPeriods(Strategy):

    def solve(self, input):
        schedules = []
        for intersection in input.intersections:
            trafic_lights = []
            for street in intersection.outgoing_streets:
                if street.end == intersection:
                    trafic_lights.append((street.name, 1))
            schedule = Schedule(intersection, trafic_lights)
            schedules.append(schedule)

        return OutputData(schedules)


class RandomPeriods(Strategy):
    def solve(self, input):
        schedules = []
        for intersection in input.intersections:
            trafic_lights = []
            for street in intersection.incoming_streets:
                trafic_lights.append((street.name, self.random.randint(1, 3)))
            schedule = Schedule(intersection.index, trafic_lights)
            schedules.append(schedule)

        return OutputData(schedules)


if __name__ == '__main__':

    directory = os.path.join(THIS_PATH, '../inputs')
    for file_name in os.listdir(directory):
        input_data = InputData(os.path.join(directory, file_name))

        my_strategy = RandomPeriods(1993)  # RandomPeriods(strategy=RandomPeriods)

        output = my_strategy.solve(input_data)

        score = calculate_score(output)

        save_output(output, file_name, score, 'marco')
