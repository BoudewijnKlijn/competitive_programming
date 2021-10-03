from qualifier.input_data import InputData
from qualifier.output_data import OutputData
from qualifier.schedule import Schedule
from qualifier.strategy import Strategy


class CarsFirstShuffle(Strategy):
    name = 'CarsFirstShuffle'

    def solve(self, input: InputData) -> OutputData:
        instersections = dict()

        cars = list(input.cars)
        self.random.shuffle(cars)

        for car in cars:
            for street in car.path[:-1]:
                if street.end not in instersections:
                    instersections[street.end] = [street.name]
                else:
                    if street.name not in instersections[street.end]:
                        instersections[street.end] = instersections[street.end] + [street.name]

        schedules = []
        for org_intersection in input.intersections:
            intersection = org_intersection.index
            if intersection in instersections:
                streets = instersections[org_intersection.index]
                schedule = Schedule(intersection, tuple([(street, 1) for street in streets]))
            else:
                schedule = Schedule(intersection, tuple())
            schedules.append(schedule)
        return OutputData(tuple(schedules))
