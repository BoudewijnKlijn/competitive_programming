from qualifier.input_data import InputData, Street
from qualifier.output_data import OutputData
from qualifier.schedule import Schedule
from qualifier.strategy import Strategy


class PlanV3(Strategy):
    name = 'PlanV3'

    def __init__(self, seed=27):

        super().__init__(seed)
        self.off_by_one = 0
        self.counted_delays = 0

    def solve(self, input_data: InputData) -> OutputData:
        intersections = dict()

        streets_with_cars = self.streets_with_car_at_light(input_data)

        def add_departure_time(intersection, street, departure_time) -> int:
            """ returns if there were already x cars departing at the same time"""
            street_departures = intersection['departure_times'][street.name]
            actual_departure_time = departure_time

            # find the first free 'departure' slot
            while actual_departure_time in street_departures:
                actual_departure_time += intersection['cycle_time']

            street_departures.append(actual_departure_time)

            return actual_departure_time

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

                if abs(diff) == 1:
                    self.off_by_one += 1

                actual_departure = add_departure_time(intersection, street, passing_time + diff)
                delay = actual_departure - passing_time
                return delay

            delay = 0
            while intersection['schedule'][schedule_slot] is not None:
                schedule_slot = (schedule_slot + 1) % intersection['cycle_time']
                delay += 1

            # should be the first from that street so no need to check the actual time.
            _ = add_departure_time(intersection, street, passing_time + delay)

            intersection['schedule'][schedule_slot] = street.name
            self.counted_delays += delay
            return delay

        for intersection in input_data.intersections:
            streets = [street for street in intersection.incoming_streets if street.name in streets_with_cars]
            intersections[intersection.index] = {
                'streets': streets,
                'cycle_time': len(streets),
                'schedule': [None] * len(streets),  # for now they are 1 second durations
                'departure_times': {street.name: list() for street in streets}
            }

        cars = list(input_data.cars)

        # This benefits from having the exact order
        streets_where_cars_start = {car.path[0] for car in cars}

        # once close to perfection perhaps stop shuffling to know the exact order of 2 cars in the same street
        # we dont know the exact order when cars arrive at the same intersection from the same street while there
        # is still a red light, so shuffle...
        self.random.shuffle(cars)


        for car in cars:
            time = add_street_to_schedule(car.path[0], passing_time=0)
            for street in car.path[1:-1]:
                time += street.time
                delay = add_street_to_schedule(street, time)
                time += delay

        schedules = []
        for intersection_nr, intersection in intersections.items():
            schedule = [(street, 1) for street in intersection['schedule']]
            schedules.append(Schedule(intersection_nr, tuple(schedule)))

        print(f'Off by 1: {self.off_by_one} of ~{input_data.n_cars * 200} intersection traversals')
        print(f'Delays as seen by the planner: {self.counted_delays}')

        return OutputData(tuple(schedules))
