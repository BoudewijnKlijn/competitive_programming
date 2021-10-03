from collections import Counter

from qualifier.input_data import InputData
from qualifier.output_data import OutputData
from qualifier.schedule import Schedule
from qualifier.strategy import Strategy


class BusyFirstV3(Strategy):
    name = 'BusyFirstV3'

    def solve(self, input: InputData) -> OutputData:
        all_streets = [car.path[:-1] for car in input.cars]
        all_streets = [item for sublist in all_streets for item in sublist]
        counted = Counter(all_streets)
        priority = {k: v for k, v in sorted(counted.items(), key=lambda item: item[1], reverse=True)}

        streets_with_cars = {street.name for street in all_streets}

        def in_bounds(value):
            return max(1, min(input.duration, value))

        def seconds(street):
            return in_bounds(counted[street] // (street.time * 10))

        schedules = []
        for intersection in input.intersections:
            trafic_lights = []

            intersection_streets = [(street, priority.get(street, 0)) for street in intersection.incoming_streets]
            intersection_streets.sort(key=lambda x: x[1])

            for street, _ in intersection_streets:
                if street.name in streets_with_cars and counted[street] >= 1:
                    trafic_lights.append((street.name, seconds(street)))

            schedule = Schedule(intersection.index,
                                tuple(trafic_lights))
            schedules.append(schedule)

        return OutputData(tuple(schedules))
