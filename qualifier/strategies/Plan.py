from qualifier.input_data import InputData, Street
from qualifier.output_data import OutputData
from qualifier.schedule import Schedule
from qualifier.strategy import Strategy


class Plan(Strategy):
    name = 'Plan'

    def solve(self, input_data: InputData) -> OutputData:
        intersections = dict()

        streets_with_cars = self.streets_with_car_at_light(input_data)

        def add_street_to_schedule(street: Street, passing_time) -> int:
            """ add the street in the optimal schedule slot if it is still empty else the first available
            assumes 1 second durations
            """
            intersection = intersections[street.end]

            schedule_slot = passing_time % intersection['cycle_time']

            if street.name in intersection['schedule']:
                given_slot = intersection['schedule'].index(street.name)
                delay = given_slot - schedule_slot
                if delay < 0:
                    delay = intersection['cycle_time'] - delay
                return delay

            delay = 0
            while intersection['schedule'][schedule_slot] is not None:
                schedule_slot = (schedule_slot + 1) % intersection['cycle_time']
                delay += 1

            intersection['schedule'][schedule_slot] = street.name
            return delay

        for intersection in input_data.intersections:
            streets = [street for street in intersection.incoming_streets if street.name in streets_with_cars]
            intersections[intersection.index] = {
                'streets': streets,
                'cycle_time': len(streets),
                'schedule': [None] * len(streets),  # for now they are 1 second durations
            }

        cars = list(input_data.cars)

        streets_where_cars_start = {car.path[0] for car in cars}

        # self.random.shuffle(cars)

        for street in streets_where_cars_start:
            add_street_to_schedule(street, passing_time=0)

        for car in cars:
            time = 1  # should probably be 1, because we processed the first streets in 0
            for street in car.path[1:-1]:
                time += street.time
                delay = add_street_to_schedule(street, time)
                time += delay

        schedules = []
        for intersection_nr, intersection in intersections.items():
            schedule = [(street, 1) for street in intersection['schedule']]
            schedules.append(Schedule(intersection_nr, tuple(schedule)))

        return OutputData(tuple(schedules))
