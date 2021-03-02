from collections import deque
import numpy as np

from qualifier.input_data import InputData
from qualifier.output_data import OutputData

from qualifier.simulatorV4.simulator_car_v4 import SimulatorCarV4
from qualifier.simulatorV4.simulator_street_v4 import SimulatorStreetV4


class SimulatorV4:
    def __init__(self, input_data: InputData, verbose: int = 0):

        self.bonus = input_data.bonus
        self.duration = input_data.duration
        self.cars = [SimulatorCarV4(path=deque(car.path)) for car in input_data.cars]
        self.verbose = verbose

        self.actions = [deque() for _ in range(self.duration)]  # list with cars, at positions equal to time of entering street

        self.streets = dict()

        self.finished = np.zeros(self.duration + 1, dtype=int)
        self.points = self.bonus + np.arange(self.duration, -1, -1)

        for street_name, street in input_data.streets.items():
            self.streets[street_name] = SimulatorStreetV4(street.time, deque())

    def init_run(self, output_data: OutputData):

        # init streets with the schedules # todo: optimize and/or rewrite
        for schedule in output_data.schedules:
            sum_other_streets_before = 0
            length_schedule = sum([d for _, d in schedule.street_duration_tuples])
            for street_name, duration in schedule.street_duration_tuples:
                self.streets[street_name].passing_times = deque([time for time in [
                    sum_other_streets_before +
                    seconds_this_street_before +
                    length_schedule * multiplier
                    for multiplier in range(2 + self.duration // length_schedule)
                    for seconds_this_street_before in range(duration)
                ] if time < self.duration])
                sum_other_streets_before += duration
            assert sum_other_streets_before == length_schedule

        if self.verbose:
            for street_name, street in self.streets.items():
                print(f'{street_name=}, {street.passing_times}')

        # init cars
        for car in self.cars:
            starting_street = car.path.popleft()
            while True:
                try:
                    passing_time = self.streets[starting_street].passing_times.popleft()
                except IndexError:
                    break

                if passing_time < car.time_passed:
                    continue  # get next passing time (green light). car has spend more time already.
                else:
                    # todo: verify if +0 or +1
                    car.time_passed = passing_time
                    self.actions[passing_time].append(car)  # add car with remaining streets to action queue
                    break

    def run(self, output_data: OutputData) -> int:
        self.init_run(output_data)

        for time in range(self.duration):
            while True:
                try:
                    car = self.actions[time].pop()
                except IndexError:
                    break
                # car enters street. ride street and check if it needs to go to another street
                street = car.path.popleft()
                car.time_passed += self.streets[street].length

                # if car is finished WITHIN duration, add it to finished
                if len(car.path) == 0 and car.time_passed <= self.duration:
                    self.finished[car.time_passed] += 1
                    continue

                while True:
                    try:
                        passing_time = self.streets[street].passing_times.popleft()
                    except IndexError:
                        break

                    if passing_time < car.time_passed:
                        continue  # get next passing time (green light). car has spend more time already.
                    else:
                        car.time_passed = passing_time
                        self.actions[passing_time].append(car)  # add car with remaining streets to action queue
                        break

        return int(np.dot(self.finished, self.points))
