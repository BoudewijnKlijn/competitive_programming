from qualifier.input_data import InputData
from qualifier.output_data import OutputData
from qualifier.schedule import Schedule
from qualifier.strategy import Strategy


class CarsFirstShuffle(Strategy):
    name = 'CarsFirstShuffle'

    def solve(self, input: InputData) -> OutputData:
        instersections = dict()

        cars = list(input.cars)
        print(f'Debug: {self.random.randint(0, 100)}')
        self.random.shuffle(cars)

        for car in cars:
            for street in car.path[:-1]:
                if street.end not in instersections:
                    instersections[street.end] = [street.name]
                else:
                    if street.name not in instersections[street.end]:
                        instersections[street.end] = instersections[street.end] + [street.name]

        schedules = []
        for intersection, streets in instersections.items():
            # maybe a bit to much? self.random.shuffle(streets)  # this does have effect on score
            schedule = Schedule(intersection, tuple([(street, 1) for street in streets]))
            schedules.append(schedule)
        return OutputData(tuple(schedules))
