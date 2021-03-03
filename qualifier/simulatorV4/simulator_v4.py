from collections import deque, defaultdict
from copy import deepcopy
import numpy as np

from qualifier.input_data import InputData
from qualifier.output_data import OutputData

from qualifier.simulatorV4.simulator_car_v4 import SimulatorCarV4
from qualifier.simulatorV4.simulator_street_v4 import SimulatorStreetV4


class SimulatorV4:
    def __init__(self, input_data: InputData, verbose: int = 0):

        self.bonus = input_data.bonus
        self.duration = input_data.duration
        self.verbose = verbose

        self.cars_init = [SimulatorCarV4(path=deque(car.path)) for car in input_data.cars]
        self.cars = list()

        self.actions_init = [list() for _ in range(self.duration)]
        self.actions = list()

        self.streets_init = {street_name: SimulatorStreetV4(street.time, deque())
                             for street_name, street in input_data.streets.items()}
        self.streets = defaultdict(SimulatorStreetV4)

        self.finished = np.zeros(self.duration + 1, dtype=int)
        self.points = self.bonus + np.arange(self.duration, -1, -1)

    def init_run(self, output_data: OutputData):

        # reset finished
        self.finished = np.zeros(self.duration + 1, dtype=int)

        # reset action queue with cars, at positions equal to time of entering street
        self.actions = deepcopy(self.actions_init)

        # add the schedules to the streets
        self.streets = deepcopy(self.streets_init)
        for schedule in output_data.schedules:
            sum_other_streets_before = 0
            length_schedule = sum([d for _, d in schedule.street_duration_tuples])
            if length_schedule == 0:
                continue
            for street_name, duration in schedule.street_duration_tuples:
                passing_times = list()
                for seconds_this_street_before in range(duration):
                    passing_times += range(sum_other_streets_before + seconds_this_street_before,
                                           self.duration,
                                           length_schedule)
                sum_other_streets_before += duration
                self.streets[street_name].passing_times = deque(sorted(passing_times))

        # reset routes of cars and add to action queue
        self.cars = deepcopy(self.cars_init)
        for car in self.cars:
            starting_street_name = car.path.popleft()
            while True:
                try:
                    passing_time = self.streets[starting_street_name].passing_times.popleft()
                except IndexError:
                    break  # no passing times available anymore for street

                if passing_time < car.time_passed:
                    self.streets[starting_street_name].n_unused_passing_times += 1  # for analysis: add unused green light
                    continue  # get next passing time (green light). car has spend more time already.
                else:
                    self.streets[starting_street_name].sum_waiting_time += \
                        passing_time - car.time_passed  # for analysis: add waiting time
                    car.time_passed = passing_time
                    self.actions[passing_time].append(car)  # add car with remaining streets to action queue
                    break  # used passing time to let a car pass, continue with next car

    def run(self, output_data: OutputData) -> int:
        self.init_run(output_data)

        for time in range(self.duration):
            for car in self.actions[time]:
                # car enters street. ride street and check if it needs to go to another street
                street_name = car.path.popleft()
                car.time_passed += self.streets[street_name].length

                # if car is finished WITHIN duration, add it to finished
                if len(car.path) == 0 and car.time_passed <= self.duration:
                    self.finished[car.time_passed] += 1
                    continue

                while True:
                    try:
                        passing_time = self.streets[street_name].passing_times.popleft()
                    except IndexError:
                        break

                    if passing_time < car.time_passed:
                        self.streets[street_name].n_unused_passing_times += 1  # for analysis: add unused green light
                        continue  # get next passing time (green light). car has spend more time already.
                    else:
                        self.streets[street_name].sum_waiting_time += \
                            passing_time - car.time_passed  # for analysis: add waiting time
                        car.time_passed = passing_time
                        self.actions[passing_time].append(car)  # add car with remaining streets to action queue
                        break  # used passing time to let a car pass, continue with next car

        return int(np.dot(self.finished, self.points))
