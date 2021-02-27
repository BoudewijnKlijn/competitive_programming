from collections import deque
from typing import List

from qualifier.input_data import InputData, Intersection, Street
from qualifier.output_data import OutputData
from qualifier.schedule import Schedule
from tqdm import tqdm


class RangeDict(dict):
    def __getitem__(self, item):
        if not isinstance(item, range):
            for key in self:
                if item in key:
                    return self[key]
            raise KeyError(item)
        else:
            return super().__getitem__(item)


class SimulatorSchedule:
    def __init__(self):
        self.street_names = []
        self.street_schedule = []

    def append(self, street_name, seconds):
        self.street_names.append(street_name)
        index = len(self.street_names) - 1
        self.street_schedule += [index] * seconds

    def __getitem__(self, item):
        return self.street_names[self.street_schedule[item]]


class SimulatorCar:
    def __init__(self, path: List[Street]):
        self.path = path
        self.name = f'{path[0].name} to {path[-1].name}'

    def __str__(self):
        return self.name


class SimulatorStreet:
    def __init__(self, exit_intersection: int, length: int, name: str):
        self.length = length
        self.exit_intersection = exit_intersection
        self.has_green = False
        self.cars = deque()
        self.name = name

    def add_car(self, car, at_traffic_light=False):
        car.path = car.path[1:]  # remove current street

        if at_traffic_light:
            self.cars.append((car, 0))
        else:
            self.cars.append((car, self.length))  # car's can move 1 step when they move on to it.

    def set_green_light(self, green: bool):
        self.has_green = green

    def execute_timestep(self) -> (List[SimulatorCar], SimulatorCar):
        # move all cars 1 step closer to the traffic light
        for i, car in enumerate(self.cars):
            self.cars[i] = (car[0], max(0, car[1] - 1))

        destination_reached = []
        for car in self.cars:
            if car[1] == 0 and len(car[0].path) == 0:
                destination_reached.append(car)
        for car in destination_reached:
            self.cars.remove(car)

        if self.has_green:
            if self.cars and self.cars[0][1] == 0:
                leaving_car = self.cars.popleft()[0]
            else:
                leaving_car = None
            return destination_reached, leaving_car
        else:
            return destination_reached, None

    def __str__(self):
        return self.name


class SimulatorIntersection:
    def __init__(self, intersection: Intersection, streets: List[SimulatorStreet]):
        self.intersection = intersection
        self.schedule = None
        self.schedule = None
        self.streets = []
        self.schedule_duration = None
        self.actual_streets = {street.name: street for street in streets}
        self.green = None

    # def add_schedule(self, schedule: Schedule):
    #       self.schedule = RangeDict()
    #     start = 0
    #     end = 0
    #     for street, duration in schedule.street_duration_tuples:
    #         if duration > 0:
    #             end = start + duration
    #             self.schedule[range(start, end)] = street
    #             start = end
    #             self.streets.append(street)
    #         else:
    #             self.streets.append(street)  # permanent red lights
    #
    #     self.schedule_duration = end
    def add_schedule(self, schedule: Schedule):
        self.schedule = SimulatorSchedule()
        for street, duration in schedule.street_duration_tuples:
            self.schedule.append(street, duration)

        self.schedule_duration = len(self.schedule.street_schedule)

    def is_green(self, street, time):
        return street == self.schedule[time % self.schedule_duration]

    def get_green(self, time):
        return self.schedule[time % self.schedule_duration]

    def execute_timestep(self, time):
        green = self.get_green(time)

        if self.green:
            self.actual_streets[self.green].set_green_light(False)
        self.actual_streets[green].set_green_light(True)
        self.green = green


class Simulator:
    def __init__(self, input_data: InputData, output_data: OutputData, verbose=True):
        """

        :type verbose: object
        """
        self.output_data = output_data
        self.input_data = input_data
        self.verbose = verbose

        self.streets = dict()
        self.intersections = dict()

        self.score = 0
        self.time = -1

        for street_name, street in input_data.streets.items():
            self.streets[street_name] = SimulatorStreet(street.end, street.time, street.name)

        for intersection in self.input_data.intersections:
            streets = [street for street in self.streets.values() if street.exit_intersection == intersection.index]
            self.intersections[intersection.index] = SimulatorIntersection(intersection.index, streets)

        for car in input_data.cars:
            starting_street = car.path[0]
            simulator_car = SimulatorCar(car.path)
            self.streets[starting_street.name].add_car(simulator_car, at_traffic_light=True)

        for schedule in output_data.schedules:
            self.intersections[schedule.intersection].add_schedule(schedule)

    def log(self, message: str):
        if self.verbose:
            print(message)

    def _score(self, cars):
        for car in cars:
            score = self.input_data.bonus + self.input_data.duration - self.time  # WARNING MIGHT BE OFF BY 1
            self.log(f'(time: {self.time}) {str(car[0])} reached destination +{score}')
            self.score += score

    def run(self) -> int:
        for _ in tqdm(range(self.input_data.duration)):
            self._execute_timestep()

        # I'm not checking yet if they arrive at their destination in their last move...
        # may need to move them a full 1 step when they move from an intersection on to the next road
        self.time += 1  # quite a few hacks here...
        for _, street in self.streets.items():
            if len(street.cars) == 0:
                continue

            destination_reached, _ = street.execute_timestep()
            self._score(destination_reached)

        return self.score

    def _execute_timestep(self):
        self.time += 1

        # update lights of each intersection
        for _, intersection in self.intersections.items():
            intersection.execute_timestep(self.time)

        moving = []

        # update cars and streets
        for _, street in self.streets.items():
            if len(street.cars) == 0:
                continue

            destination_reached, moving_to_next_street = street.execute_timestep()
            self._score(destination_reached)
            if moving_to_next_street is not None:
                moving.append(moving_to_next_street)

                # now that all streets have been processed we can move the cars (we dont want to move them twice in 1 timestep)
        for car in moving:
            self.log(f'(time: {self.time}) {car}:\n\t\tmoving onto {car.path[0].name}')
            street = car.path[0]
            self.streets[street.name].add_car(car)
