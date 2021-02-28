from qualifier.output_data import OutputData
from qualifier.schedule import Schedule
from qualifier.strategy import Strategy


class SmartRandom(Strategy):
    name = 'SmartRandom'

    def __init__(self, seed, max_duration):

        super().__init__(seed=seed)
        self.max_duration = max_duration

    def solve(self, input_data):

        # driving trough! them (if they only finish there we dont need to do any traffic lights schedule either...
        all_streets = [car.path[:-1] for car in input_data.cars]
        streets_with_cars = {item for sublist in all_streets for item in sublist}

        schedules = []
        for intersection in input_data.intersections:
            traffic_lights = []
            incoming_streets = list(intersection.incoming_streets)
            self.random.shuffle(incoming_streets)
            for street in incoming_streets:
                if street in streets_with_cars:
                    traffic_lights.append((street.name, self.random.randint(1, self.max_duration)))
            schedule = Schedule(intersection.index, traffic_lights)
            schedules.append(schedule)

        return OutputData(tuple(schedules))
