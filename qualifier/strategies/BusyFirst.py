from collections import Counter

import numpy as np

from qualifier.input_data import InputData
from qualifier.output_data import OutputData
from qualifier.schedule import Schedule
from qualifier.strategy import Strategy


class BusyFirst(Strategy):
    name = 'BusyFirst'

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
            if counted[street] <= mean_value - std_value * 0:
                return 1
            if counted[street] <= mean_value + std_value * .5:
                return 2
            if counted[street] <= mean_value + std_value * .1:
                return 3
            if counted[street] <= mean_value + std_value * 2:
                return 4
            if counted[street] <= mean_value + std_value * 4:
                return 5
            else:
                return 6

        schedules = []
        for intersection in input.intersections:
            trafic_lights = []
            for street in intersection.incoming_streets:
                if street.name in streets_with_cars:
                    trafic_lights.append((street.name, seconds(street)))

            schedule = Schedule(intersection.index, tuple(trafic_lights))
            schedules.append(schedule)

        return OutputData(tuple(schedules))
