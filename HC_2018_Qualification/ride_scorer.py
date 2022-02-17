import os

from HC_2018_Qualification.car_schedules import CarSchedules
from HC_2018_Qualification.city_data import CityData, Location
from valcon.scorer import Scorer

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
    def manhattan_distance(position1: Location, position2: Location) -> int:
        return abs(position1.x - position2.x) + abs(position1.y - position2.y)

    def calculate(self, output_data: CarSchedules) -> int:
        score = 0
        for _, ride_ids in output_data.car_schedules:
            time = 0
            vehicle_position = Location(0, 0)
            for ride_id in ride_ids:
                # Drive to pickup.
                pickup_position = self.rides[ride_id].start
                travel_distance = self.manhattan_distance(vehicle_position, pickup_position)
                vehicle_position = pickup_position
                time += travel_distance

                # Stop simulation if out of time.
                if time > self.steps:
                    break

                # Bonus point if vehicle arrives at pickup at before or on the earliest time.
                if time <= self.rides[ride_id].earliest:
                    score += self.bonus
                else:
                    # Ride cannot start before pickup time. Update time to at least the pickup time.
                    time = max(time, self.rides[ride_id].earliest)

                # Drive to drop off.
                drop_off_position = self.rides[ride_id].end
                travel_distance = self.manhattan_distance(vehicle_position, drop_off_position)
                vehicle_position = drop_off_position
                time += travel_distance

                # Stop simulation if out of time.
                if time > self.steps:
                    break

                # If ride is on time, add ride travel distance to score.
                if time < self.rides[ride_id].latest:
                    score += travel_distance

                # Continue with next ride.
            # Continue with next vehicle.
        return score


if __name__ == '__main__':
    schedules = [
        [1, [0]],
        [2, [2, 1]]
    ]
    output = CarSchedules(schedules)

    input_data = CityData(os.path.join(THIS_PATH, 'input', 'a_example.in'))
    ride_scorer = RideScore(input_data)
    score = ride_scorer.calculate(output_data=output)
    print(score)
