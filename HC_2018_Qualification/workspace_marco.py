import glob
import os
import time
from copy import copy

import numpy as np
from dataclasses import dataclass

from HC_2018_Qualification.car_schedules import CarSchedules, CarSchedule
from HC_2018_Qualification.city_data import CityData, Ride
from HC_2018_Qualification.location import Location
from HC_2018_Qualification.ride_scorer import RideScore

from valcon import Strategy, InputData, OutputData
from valcon.utils import best_score, generate_file_name, get_problem_name

THIS_PATH = os.path.abspath(os.path.dirname(__file__))


# class PayToWin(Strategy):
#
#     def solve(self, input_data: CityData) -> CarSchedules:
#         ordered_rides = input_data.rides.copy()
#         ordered_rides.sort(key=lambda ride: ride.max_payout)

@dataclass
class Car:
    location: Location
    rides: list[Ride]


class SimulateCity(Strategy):

    def best_ride(self, car: Car, rides: list, step: int):
        return rides[0]

    def solve(self, input_data: CityData) -> CarSchedules:
        unused_cars = [Car(Location(0, 0)) for _ in range(input_data.vehicles)]

        timeline = [[] for _ in range(input_data.steps)]

        unfinished_rides = input_data.rides.copy()

        for step in range(input_data.steps):
            for car in unused_cars:
                car = unused_cars.pop(0)
                best_ride = self.best_ride(car, unfinished_rides, step)
                car.rides.append(best_ride.id)
                timeline_position = get_distance(car.location, best_ride.start) + get_distance(best_ride.start,
                                                                                               best_ride.end)


class MarcoRandom(Strategy):

    def solve(self, input_data: CityData) -> CarSchedules:
        P = len(input_data.rides)
        I = input_data.vehicles
        split_points = np.random.choice(P - 2, I - 1, replace=False) + 1
        split_points.sort()

        copied_rides = input_data.rides.copy()
        self.random.shuffle(copied_rides)

        result = np.split(input_data.rides, split_points)
        car_schedules = []
        for raw in result:
            car_schedules.append(CarSchedule(len(raw), [x.id for x in raw]))

        return CarSchedules(car_schedules)


if __name__ == '__main__':
    directory = os.path.join(THIS_PATH, 'input')
    output_directory = os.path.join(THIS_PATH, 'output')

    files = glob.glob(os.path.join(directory, "*.in"))

    current_best = best_score(output_directory)

    for problem_file in files:
        problem_name = get_problem_name(problem_file)
        problem = CityData(problem_file)
        print(problem)

        solver = MarcoRandom()
        scorer = RideScore(problem)

        start = time.perf_counter()
        solution = solver.solve(problem)
        duration = time.perf_counter() - start

        score = scorer.calculate(solution)

        print(f'{problem_file} Score: {score} ({duration:0.0f}s)')

        out_file = generate_file_name(problem_file, score, solver)
        print(f'Writing {out_file}')

        if current_best[problem_name] < score:
            solution.save(os.path.join(output_directory, out_file))

    print(best_score(output_directory))
