from qualifier.input_data import InputData
from qualifier.output_data import OutputData
from qualifier.schedule import Schedule
from qualifier.strategy import Strategy


class CarsFirst(Strategy):
    name = 'CarsFirst'

    def solve(self, input: InputData) -> OutputData:
        instersections = dict()

        cars = list(input.cars)
        self.random.shuffle(cars)  # shuffle the cars with the same total path length

        sorted(cars, key=lambda car_: sum([street_.time for street_ in car_.path[1:]]))

        for car in cars:
            for street in car.path[:-1]:
                if street.end not in instersections:
                    instersections[street.end] = [street.name]
                else:
                    if street.name not in instersections[street.end]:
                        instersections[street.end] = instersections[street.end] + [street.name]

        schedules = []
        for intersection, streets in instersections.items():
            schedule = Schedule(intersection, tuple([(street, 1) for street in streets]))
            schedules.append(schedule)
        return OutputData(tuple(schedules))
