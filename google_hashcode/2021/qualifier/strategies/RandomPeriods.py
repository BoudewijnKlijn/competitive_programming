from qualifier.output_data import OutputData
from qualifier.schedule import Schedule
from qualifier.strategy import Strategy


class RandomPeriods(Strategy):
    name = 'RandomPeriods'

    def __init__(self, seed=27, max_period=3):

        super().__init__(seed=seed)
        self.max_period = max_period

    def solve(self, input_data):
        street_with_cars = self.streets_with_car_at_light(input_data)

        schedules = []
        for intersection in input_data.intersections:
            traffic_lights = []
            for street in intersection.incoming_streets:
                if street.name in street_with_cars:
                    traffic_lights.append((street.name, self.random.randint(1, self.max_period)))
            schedule = Schedule(intersection.index, tuple(traffic_lights))
            schedules.append(schedule)

        return OutputData(tuple(schedules))
