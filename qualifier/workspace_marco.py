import os

from qualifier.calculate_score import calculate_score
from qualifier.input_data import InputData
from qualifier.output_data import OutputData
from qualifier.schedule import Schedule
from qualifier.strategy import Strategy
from qualifier.util import save_output

from collections import Counter
import numpy as np

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


class AtleastOneCar(Strategy):
    def solve(self, input):

        all_streets = [car.path for car in input.cars]
        streets_with_cars = {item for sublist in all_streets for item in sublist}

        schedules = []
        for intersection in input.intersections:
            trafic_lights = []
            for street in intersection.incoming_streets:
                if street.name in streets_with_cars:
                    trafic_lights.append((street.name, 1))
            if len(trafic_lights):
                schedule = Schedule(intersection.index, trafic_lights)
                schedules.append(schedule)

        return OutputData(schedules)


class CarsFirst(Strategy):
    def solve(self, input: InputData) -> OutputData:
        instersections = dict()

        cars = input.cars
        sorted(cars, key=lambda car_: sum([street_.time for street_ in car_.path]))

        for car in cars:
            for street in car.path:
                if street.end not in instersections:
                    instersections[street.end] = [street.name]
                else:
                    if street.name not in instersections[street.end]:
                        instersections[street.end] = instersections[street.end] + [street.name]

        schedules = []
        for intersection, streets in instersections.items():
            schedule = Schedule(intersection, [(street, 1) for street in streets])
            schedules.append(schedule)
        return OutputData(schedules)


class BusyFirst(Strategy):
    def solve(self, input: InputData) -> OutputData:
        all_streets = [car.path for car in input.cars]
        all_streets = [item for sublist in all_streets for item in sublist]
        counted = Counter(all_streets)
        priority = {k: v for k, v in sorted(counted.items(), key=lambda item: item[1], reverse=True)}
        values = list(priority.values())
        mean_value = np.mean(values)
        std_value = np.std(values)

        streets_with_cars = {street.name for street in all_streets}

        def seconds(street):
            if counted[street] < mean_value - std_value:
                return 1
            if counted[street] <= mean_value:
                return 1
            if counted[street] > mean_value:
                return 3
            if counted[street] > mean_value + std_value:
                return 4

            print('should not happen')
            return 1

        schedules = []
        for intersection in input.intersections:
            trafic_lights = []
            for street in intersection.incoming_streets:
                if street.name in streets_with_cars:
                    trafic_lights.append((street.name, seconds(street)))
            if len(trafic_lights):
                schedule = Schedule(intersection.index, trafic_lights)
                schedules.append(schedule)

        return OutputData(schedules)


if __name__ == '__main__':

    directory = os.path.join(THIS_PATH, '../inputs')
    for file_name in os.listdir(directory):
        input_data = InputData(os.path.join(directory, file_name))

        my_strategy = BusyFirst(1993)  # RandomPeriods(strategy=RandomPeriods)

        output = my_strategy.solve(input_data)

        score = calculate_score(output)

        save_output(output, file_name, score, 'marco')
