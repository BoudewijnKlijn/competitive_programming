from collections import deque
import numpy as np

from qualifier.input_data import InputData
from qualifier.output_data import OutputData
from qualifier.schedule import EvaluatedSchedule
from qualifier.simulator.simulator import Simulator

from qualifier.simulatorV5.simulator_car_v5 import SimulatorCarV5
from qualifier.simulatorV5.simulator_street_v5 import SimulatorStreetV5
from qualifier.simulatorV5.traffic_light import green_light_times


class SimulatorV5(Simulator):
    def __init__(self, input_data: InputData, verbose: int = 0):

        self.bonus = input_data.bonus
        self.duration = input_data.duration
        self.verbose = verbose

        self.car_paths = [[street for street in car.path] for car in input_data.cars]

        self.cars = list()

        self.actions = list()

        self.streets_input = input_data.streets
        self.streets = {street_name: SimulatorStreetV5(street.time)
                        for street_name, street in self.streets_input.items()}

        self.finished = np.zeros(self.duration + 1, dtype=int)
        self.points = self.bonus + np.arange(self.duration, -1, -1)

        self.all_times = list(range(self.duration))

    def reset(self):
        # reset finished
        self.finished = np.zeros(self.duration + 1, dtype=int)

        # reset action queue with cars, at positions equal to time of entering street
        self.actions = [list() for _ in range(self.duration)]

        # reset streets
        for street in self.streets.values():
            street.clear()

    def setup_car_routes(self):
        # reset routes of cars and add to action queue
        for car_path in self.car_paths:
            car = SimulatorCarV5(path=deque(car_path))
            starting_street_name = car.path.popleft()
            starting_street = self.streets[starting_street_name]
            while True:
                try:
                    passing_time = next(starting_street.passing_times)
                except StopIteration:
                    break  # no passing times available anymore for street

                if passing_time < car.time_passed:
                    starting_street.n_unused_passing_times += 1  # for analysis: add unused green light
                    continue  # get next passing time (green light). car has spend more time already.
                else:
                    starting_street.sum_waiting_time += \
                        passing_time - car.time_passed  # for analysis: add waiting time
                    car.time_passed = passing_time
                    self.actions[passing_time].append(car)  # add car with remaining streets to action queue
                    break  # used passing time to let a car pass, continue with next car

    def add_schedules_to_streets(self, output_data):
        # add the schedules to the streets
        for schedule in output_data.schedules:
            length_schedule = sum([d for _, d, *_ in schedule.street_duration_tuples])
            if length_schedule == 0:
                continue

            time = 0
            for street_name, duration, *_ in schedule.street_duration_tuples:
                self.streets[street_name].passing_times = green_light_times(length_schedule, time,
                                                                            (time := time + duration),
                                                                            self.duration)

    def init_run(self, output_data: OutputData):
        self.reset()

        self.add_schedules_to_streets(output_data)

        self.setup_car_routes()

    def run(self, output_data: OutputData) -> (int, OutputData):
        self.init_run(output_data)

        for time in self.all_times:
            for car in self.actions[time]:
                # car enters street. ride street and check if it needs to go to another street
                street_name = car.path.popleft()
                street = self.streets[street_name]
                car.time_passed += street.length

                # if car is finished WITHIN duration, add it to finished
                if len(car.path) == 0 and car.time_passed <= self.duration:
                    self.finished[car.time_passed] += 1
                    continue

                while True:
                    try:
                        passing_time = next(street.passing_times)
                    except StopIteration:
                        break

                    if passing_time < car.time_passed:
                        street.n_unused_passing_times += 1  # for analysis: add unused green light
                        continue  # get next passing time (green light). car has spend more time already.
                    else:
                        street.sum_waiting_time += \
                            passing_time - car.time_passed  # for analysis: add waiting time
                        car.time_passed = passing_time
                        self.actions[passing_time].append(car)  # add car with remaining streets to action queue
                        break  # used passing time to let a car pass, continue with next car

        evaluated_schedule = []
        for schedule in output_data.schedules:
            new_schedule = []
            for street in schedule.street_duration_tuples:
                new_schedule.append((street[0], street[1], self.streets[street[0]].sum_waiting_time))
            evaluated_schedule.append(EvaluatedSchedule(schedule.intersection, tuple(new_schedule)))

        return int(np.dot(self.finished, self.points)), OutputData(tuple(evaluated_schedule))
