from collections import Counter

from qualifier.input_data import InputData
from qualifier.output_data import OutputData
from qualifier.schedule import Schedule
from qualifier.strategy import Strategy


class Eliot(Strategy):
    name = 'Eliot'

    def solve(self, input: InputData) -> OutputData:
        all_streets = [car.path for car in input.cars]
        all_streets = [item for sublist in all_streets for item in sublist]
        counted = Counter(all_streets)
        priority = {k: v for k, v in sorted(counted.items(), key=lambda item: item[1], reverse=True)}

        instersections = dict()

        for street, count in priority.items():
            if street.end not in instersections:
                instersections[street.end] = [(street.name, min(input.duration, count))]
            else:
                if street.name not in instersections[street.end]:
                    instersections[street.end] = instersections[street.end] + [
                        (street.name, min(input.duration, count))]

        schedules = []
        for intersection, streets in instersections.items():
            schedule = Schedule(intersection, [(street[0], street[1]) for street in streets])
            schedules.append(schedule)
        return OutputData(tuple(schedules))
