from collections import Counter

import numpy as np

from qualifier.input_data import InputData
from qualifier.output_data import OutputData
from qualifier.schedule import Schedule
from qualifier.strategy import Strategy


class BusyFirstV2(Strategy):
    name = 'BusyFirstV2'

    def solve(self, input: InputData) -> OutputData:
        all_streets = [car.path[:-1] for car in input.cars]
        all_streets = [item.name for sublist in all_streets for item in sublist]
        counted = Counter(all_streets)
        priority = {k: v for k, v in sorted(counted.items(), key=lambda item: item[1], reverse=True)}
        values = list(priority.values())
        mean_value = np.mean(values)
        std_value = np.std(values)

        streets_with_cars = {*all_streets}

        step_size = max(1, input.duration // input.n_cars)

        def step(multiplier):
            return min(input.duration, step_size * multiplier)

        def seconds(street):
            return int(max(1, step((counted[street] - mean_value) // std_value)))

        schedules = []
        for intersection in input.intersections:
            trafic_lights = []
            for street in intersection.incoming_streets:
                if street.name in streets_with_cars:
                    trafic_lights.append((street.name, seconds(street)))

            schedule = Schedule(intersection.index, tuple(trafic_lights))
            schedules.append(schedule)

        return OutputData(tuple(schedules))
