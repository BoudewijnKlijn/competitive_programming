from qualifier.input_data import InputData
from qualifier.output_data import OutputData
from qualifier.schedule import Schedule
from qualifier.strategy import Strategy


class DropOutCars(Strategy):
    name = 'DropOutCars'

    def solve(self, input: InputData, drop_percentage=0.03) -> OutputData:
        """ 3% of cars never make it so maybe remove a few cars at random hoping removing some bottlenecks? """
        instersections = dict()

        cars = input.cars
        cars = self.random.sample(list(cars), int(len(cars) * (1 - drop_percentage)))

        for car in cars:
            for street in car.path[:-1]:
                if street.end not in instersections:
                    instersections[street.end] = [street.name]
                else:
                    if street.name not in instersections[street.end]:
                        instersections[street.end] = instersections[street.end] + [street.name]

        schedules = []
        for intersection, streets in instersections.items():
            self.random.shuffle(streets)  # this does have effect on score
            schedule = Schedule(intersection, tuple([(street, 1) for street in streets]))
            schedules.append(schedule)
        return OutputData(tuple(schedules))
