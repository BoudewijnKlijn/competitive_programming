from qualifier.input_data import InputData, Street
from qualifier.output_data import OutputData
from qualifier.schedule import Schedule
from qualifier.strategy import Strategy


class Plan(Strategy):
    name = 'Plan'

    def __init__(self, seed=27, drop_out=0.0):
        """ Drop rate: potential score
         - 0.00: 3.9m (actual 1.6m)
         - 0.10: 3.6m (actual 1.5m)
         - 0.20: 3.2m (actual 1.4m)
         - 0.48: 2.0m (actual 1.1m)
        """

        super().__init__(seed=seed)
        self.drop_out = drop_out

    def solve(self, input_data: InputData) -> OutputData:
        intersections = dict()

        streets_with_cars = self.streets_with_car_at_light(input_data)

        for intersection in input_data.intersections:
            streets = [street for street in intersection.incoming_streets if street.name in streets_with_cars]
            intersections[intersection.index] = {
                'streets': streets,
                'cycle_time': len(streets),
                'schedule': [None] * len(streets),  # for now they are 1 second durations
            }

        cars = list(input_data.cars)
        self.random.shuffle(cars)

        streets_where_cars_start = {car.path[0] for car in cars}

        def add_street_to_schedule(street: Street, passing_time) -> int:
            """ add the street in the optimal schedule slot if it is still empty else the first availalbe
            assumes 1 second durations
            """
            intersection = intersections[street.end]

            schedule_slot = passing_time % intersection['cycle_time']

            if street.name in intersection['schedule']:
                # lets hope for the best but we can improve upon this
                given_slot = intersection['schedule'].index(street.name)
                diff = given_slot - schedule_slot
                if diff < 0:
                    diff = intersection['cycle_time'] - diff
                return diff

            delay = 0
            while intersection['schedule'][schedule_slot] is not None:
                schedule_slot = (schedule_slot + 1) % intersection['cycle_time']
                delay += 1

            intersection['schedule'][schedule_slot] = street.name
            return delay

        for street in streets_where_cars_start:
            add_street_to_schedule(street, passing_time=0)

        for car in cars:
            time = 0
            for street in car.path[1:-1]:
                time += street.time
                delay = add_street_to_schedule(street, time)
                time += delay

        schedules = []
        for intersection_nr, intersection in intersections.items():
            schedule = [(street, 1) for street in intersection['schedule'] if street is not None]
            schedules.append(Schedule(intersection_nr, tuple(schedule)))

        return OutputData(tuple(schedules))
