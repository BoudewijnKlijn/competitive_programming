import os

from HC_2018_Qualification.car_schedules import CarSchedules, CarSchedule
from HC_2018_Qualification.city_data import CityData
from HC_2018_Qualification.location import Location
from valcon.scorer import Scorer

THIS_PATH = os.path.abspath(os.path.dirname(__file__))
OUTPUT_DIRECTORY = os.path.join(THIS_PATH, 'output')


def get_distance(position1: Location, position2: Location) -> int:
    """Manhattan distance."""
    return abs(position1.x - position2.x) + abs(position1.y - position2.y)


class RideScore(Scorer):
    """
    Calculate score for output rides.

    Each vehicle picks rides in the order they appear in the output file.
    The ride ids correspond to lines in the input files.

    Example output:
    1 0      this vehicle is assigned 1 ride: [0]
    2 2 1    this vehicle is assigned 2 rides: [2, 1]
    """

    def __init__(self, input_data: CityData, verbose: bool = True):
        self.rides = input_data.rides
        self.steps = input_data.steps
        self.bonus = input_data.bonus
        self.verbose = verbose

    def calculate(self, output_data: CarSchedules) -> int:
        rides_done = set()
        distance_score = 0
        bonus_score = 0
        n_bonus = 0
        n_rides_possible = len(self.rides)
        n_rides_started = 0
        n_rides_finished = 0
        for schedules in output_data.car_schedules:
            ride_ids = schedules.rides
            time = 0
            vehicle_position = Location(0, 0)
            for ride_id in ride_ids:
                # Make sure ride is not assigned twice.
                if ride_id in rides_done:
                    raise ValueError(f'Ride {ride_id} is assigned twice')

                rides_done.add(ride_id)
                n_rides_started += 1

                # Drive to pickup.
                pickup_position = self.rides[ride_id].start
                travel_distance = get_distance(vehicle_position, pickup_position)
                vehicle_position = pickup_position
                time += travel_distance

                # Stop simulation if out of time.
                if time > self.steps:
                    break

                # Bonus point if vehicle arrives at pickup at before or on the earliest time.
                if time <= self.rides[ride_id].earliest:
                    n_bonus += 1
                else:
                    # Ride cannot start before pickup time. Update time to at least the pickup time.
                    time = max(time, self.rides[ride_id].earliest)

                # Drive to drop off.
                drop_off_position = self.rides[ride_id].end
                travel_distance = get_distance(vehicle_position, drop_off_position)
                vehicle_position = drop_off_position
                time += travel_distance

                # Stop simulation if out of time.
                if time > self.steps:
                    break

                # If ride is on time, add ride travel distance to score.
                if time < self.rides[ride_id].latest:
                    distance_score += travel_distance
                    n_rides_finished += 1

                # Continue with next ride.
            # Continue with next vehicle.

        if self.verbose:
            bonus_score = n_bonus * self.bonus
            print(f'{distance_score=}, {bonus_score=}, {n_bonus=}\n'
                  f'{n_rides_possible=}, {n_rides_started=} ({n_rides_started / n_rides_possible:.2f}), '
                  f'{n_rides_finished=} ({n_rides_finished / n_rides_possible:.2f} / '
                  f'{n_rides_finished / n_rides_started:.2f})')
        return distance_score + bonus_score


if __name__ == '__main__':
    schedules = [
        CarSchedule(1, [0]),
        CarSchedule(2, [2, 1]),
    ]
    output = CarSchedules(schedules)

    input_data = CityData(os.path.join(THIS_PATH, 'input', 'a_example.in'))
    ride_scorer = RideScore(input_data)
    score = ride_scorer.calculate(output_data=output)
    print(score)
