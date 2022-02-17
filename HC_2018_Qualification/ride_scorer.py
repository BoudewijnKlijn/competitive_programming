import os
from typing import Iterable

from valcon import OutputData
from valcon import Strategy
from valcon.scorer import Scorer

from HC_2018_Qualification.city_data import CityData
from HC_2018_Qualification.car_schedules import CarSchedule

THIS_PATH = os.path.abspath(os.path.dirname(__file__))
OUTPUT_DIRECTORY = os.path.join(THIS_PATH, 'output')


class RideScore(Scorer):
    """
    Calculate score for output rides.

    Each vehicle picks rides in the order they appear in the output file.
    The ride ids correspond to lines in the input files.

    Example output:
    1 0      this vehicle is assigned 1 ride: [0]
    2 2 1    this vehicle is assigned 2 rides: [2, 1]
    """
    def __init__(self, input_data: CityData):
        self.rides = input_data.rides
        self.steps = input_data.steps
        self.bonus = input_data.bonus

    @staticmethod
    def manhattan_distance(position1, position2):
        return abs(position1[0] - position2[0]) + abs(position1[1] - position2[1])

    def calculate(self, output_data) -> int:
        score = 0
        for vehicle in output_data:
            ride_ids = [ride_id for ride_id in vehicle.rides]
            time = 0
            vehicle_position = (0, 0)
            for ride_id in ride_ids:
                # drive to the first pickup
                pickup_position = self.rides[ride_id].pickup
                travel_distance = self.manhattan_distance(vehicle_position, pickup_position)
                time += travel_distance

                # first check if bonus points
                if time == self.rides[ride_id].earliest_start:
                    score += self.rides[ride_id].bonus
                # ride cannot start before pickup time. update time to at least the pickup time
                time = max(time, self.rides[ride_id].earliest_start)

        for customer in self.pizza_demands.customers:
            if customer.will_order(output_data):
                score += 1
        return score

    def calculate_multi(self, multi_output_data: Iterable[OutputData]) -> Iterable[int]:
        pass

    def repeat_solve(self, strategy: Strategy, n_repetitions: int) -> Strategy:
        for seed in range(n_repetitions):
            strategy.change_seed(seed)
            solution = strategy.solve(self.pizza_demands)
            score = self.calculate(solution)
            if strategy.best_score is None or score > strategy.best_score:
                strategy.best_seed = seed
                strategy.best_score = score
                strategy.best_output = solution
                if solution is None:
                    print(seed, 'None')
        return strategy
