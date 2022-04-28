import glob
import os
import time
from copy import copy

import numpy as np
from dataclasses import dataclass

from HC_2018_Qualification.car_schedules import CarSchedules, CarSchedule
from HC_2018_Qualification.city_data import CityData, Ride
from HC_2018_Qualification.location import Location
from HC_2018_Qualification.ride_scorer import RideScore, get_distance

from valcon import Strategy, InputData, OutputData
from valcon.utils import best_score, generate_file_name, get_problem_name, flatten

THIS_PATH = os.path.abspath(os.path.dirname(__file__))


@dataclass
class Car:
    location: Location
    rides: list[Ride]


class SimCity(Strategy):
    def __init__(self):
        super().__init__()
        self.bonus = 0

    def best_ride(self, car: Car, rides: list, step: int):

        scoring_rides = [ride for ride in rides
                         if
                         step + get_distance(car.location, ride.start) + get_distance(ride.start,
                                                                                      ride.end) <= ride.latest
                         ]

        def ride_score(ride: Ride):
            has_bonus = step + get_distance(car.location, ride.start) <= ride.earliest

            score = self.bonus if has_bonus else 0
            score += ride.max_payout - get_distance(car.location, ride.start) * 2

            return score

        scoring_rides.sort(key=lambda ride: ride_score(ride), reverse=True)

        if not scoring_rides:
            return None

        return scoring_rides[0]

    def solve(self, input_data: CityData) -> CarSchedules:
        self.bonus = input_data.bonus

        cars = [Car(Location(0, 0), []) for _ in range(input_data.vehicles)]

        timeline = [[] for _ in range(input_data.steps)]
        timeline[0] = cars  # we are not modifying this list so this is ok
        unfinished_rides = input_data.rides.copy()
        print(f"{len(unfinished_rides)} rides to start with")

        for step in range(input_data.steps):
            unused_cars = timeline[step]
            for car in unused_cars:
                best_ride = self.best_ride(car, unfinished_rides, step)
                if not best_ride:
                    continue
                unfinished_rides.remove(best_ride)

                car.rides.append(best_ride.id)

                timeline_position = max(
                    (step + get_distance(car.location, best_ride.start)),
                    best_ride.earliest
                ) + get_distance(best_ride.start, best_ride.end)

                if timeline_position < input_data.steps:
                    timeline[timeline_position].append(car)
                else:
                    print('not allowed')

        print(f'{len(flatten(car.rides for car in cars))=}')

        return CarSchedules([CarSchedule(len(car.rides), car.rides) for car in cars])


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
        print(f'--- {problem_name} ---')
        problem = CityData(problem_file)

        solver = SimCity()
        scorer = RideScore(problem)

        start = time.perf_counter()
        solution = solver.solve(problem)
        duration = time.perf_counter() - start

        score = scorer.calculate(solution)

        print(f'{problem_file} Score: {score} ({duration:0.0f}s)')

        out_file = generate_file_name(problem_file, score, solver)

        if score > current_best[problem_name]:
            print(f'Writing {out_file}')
            solution.save(os.path.join(output_directory, out_file))
        else:
            print(f'No improvement for {problem_name}')

        print('\n')

    print(best_score(output_directory))
