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
        self.verbose = verbose

        self.cars_input = input_data.cars
        self.cars = list()

        self.actions = list()

        self.streets_input = input_data.streets
        self.streets = dict()

        self.finished = np.zeros(self.duration + 1, dtype=int)
        self.points = self.bonus + np.arange(self.duration, -1, -1)

    def init_run(self, output_data: OutputData):

        # reset finished
        self.finished = np.zeros(self.duration + 1, dtype=int)

        # reset action queue with cars, at positions equal to time of entering street
        self.actions = [list() for _ in range(self.duration)]

        # add the schedules to the streets
        self.streets = {street_name: SimulatorStreetV4(street.time, deque())
                        for street_name, street in self.streets_input.items()}

        for schedule in output_data.schedules:
            length_schedule = sum([d for _, d in schedule.street_duration_tuples])
            if length_schedule == 0:
                continue
            all_times = list(range(self.duration))
            time = 0
            while time < self.duration:
                for street_name, duration in schedule.street_duration_tuples:
                    self.streets[street_name].passing_times += all_times[time: (time := time + duration)]

        # reset routes of cars and add to action queue
        self.cars = [SimulatorCarV4(path=deque(car.path)) for car in self.cars_input]
        for car in self.cars:
            starting_street_name = car.path.popleft()
            while True:
                try:
                    passing_time = self.streets[starting_street_name].passing_times.popleft()
                except IndexError:
                    break  # no passing times available anymore for street

                if passing_time < car.time_passed:
                    self.streets[
                        starting_street_name].n_unused_passing_times += 1  # for analysis: add unused green light
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
