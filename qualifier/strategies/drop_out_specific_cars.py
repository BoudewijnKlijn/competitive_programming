from collections import Counter

from qualifier.input_data import InputData
from qualifier.output_data import OutputData
from qualifier.schedule import Schedule
from qualifier.strategy import Strategy


class DropOutSpecificCars(Strategy):
    name = 'DropOutSpecificCars'

    def __init__(self, seed=27, drop_ratio=0.05):
        super().__init__(seed=seed)
        self.drop_ratio = drop_ratio

    def solve(self, input: InputData) -> OutputData:
        """ drop cars that have many streets that only they use for more optimal green lights """
        instersections = dict()

        cars = list(input.cars)

        cars_to_drop = int(len(cars) * self.drop_ratio)

        all_streets = [car.path[:-1] for car in input.cars]
        all_streets = [item.name for sublist in all_streets for item in sublist]
        counted = Counter(all_streets)

        for car in cars:
            car.street_score = 0
            for street in car.path:
                if counted[street.name] == 1:
                    car.street_score += 1

        # highest car that go to a single street
        cars.sort(key=lambda car: car.street_score, reverse=True)
        cars = cars[cars_to_drop:]

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
