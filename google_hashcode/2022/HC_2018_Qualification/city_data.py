from dataclasses import dataclass

from HC_2018_Qualification.location import Location
from valcon import InputData


@dataclass
class Ride:
    id: int
    start: Location
    end: Location
    earliest: int
    latest: int

    @property
    def max_payout(self) -> int:
        return abs(self.end.x - self.start.x) + abs(self.end.y - self.start.y)


class CityData(InputData):
    def __init__(self, file_name: str):
        with open(file_name, 'r') as file:
            city_data, *raw_rides = file.readlines()

        rows, columns, vehicles, rides, bonus, steps = [int(x) for x in city_data.split()]
        self.rows = rows
        self.columns = columns
        self.vehicles = vehicles
        self.rides = [self.parse_ride(i, x) for i, x in enumerate(raw_rides)]
        self.bonus = bonus
        self.steps = steps

    @staticmethod
    def parse_ride(ride_id: int, raw_ride):
        start_x, start_y, finish_x, finish_y, earliest_start, latest_finish = [int(x) for x in raw_ride.split()]

        return Ride(ride_id, Location(start_x, start_y), Location(finish_x, finish_y), earliest_start, latest_finish)
