from qualifier.input_data import InputData
from qualifier.output_data import OutputData
from qualifier.schedule import Schedule
from qualifier.strategy import Strategy


class CarsFirstShuffleDropOut(Strategy):
    name = 'CarsFirstShuffleDropOut'

    def __init__(self, seed=27, drop_out=0.0):
        """ Drop rate: potential score
         - 0.00: 3.9m (actual 1.6m)
         - 0.10: 3.6m (actual 1.5m)
         - 0.20: 3.2m (actual 1.4m)
         - 0.48: 2.0m (actual 1.1m)
        """

        super().__init__(seed=seed)
        self.drop_out = drop_out

    def solve(self, input: InputData) -> OutputData:
        instersections = dict()

        cars = list(input.cars)
        sorted(cars, key=lambda car_: sum([street_.time for street_ in car_.path[1:]]))

        if self.drop_out > 0:
            cars_drop = int(len(cars) // (1 / self.drop_out))
            cars = cars[:-cars_drop]

        potential_score = sum(
            [input.duration - sum([street.time for street in car.path]) + input.bonus for car in cars])
        print(f'drop ratio: {self.drop_out} => {len(cars)} cars, potential score: {potential_score}')

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
                self.random.shuffle(streets)
                schedule = Schedule(intersection, tuple([(street, 1) for street in streets]))
            else:
                # schedules = [(street.name, 0) for street in org_intersection.incoming_streets]
                # schedule = Schedule(intersection, tuple(schedules))
                schedule = Schedule(intersection, tuple())
            schedules.append(schedule)
        return OutputData(tuple(schedules))
