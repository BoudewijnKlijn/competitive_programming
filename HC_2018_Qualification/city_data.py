from dataclasses import dataclass

from valcon import InputData


@dataclass
class Location:
    x: int
    y: int


class Ride:
    def __init__(self, start, end, earliest, latest):
        self.start = start
        self.end = end
        self.earliest = earliest
        self.latest = latest

    def __str__(self):
        return '{} {} {} {}'.format(self.start, self.end, self.earliest, self.latest)

    def __repr__(self):
        return self.__str__()


class CityData(InputData):
    def __init__(self, file_name: str):
        with open(file_name, 'r') as file:
            city_data, *raw_rides = file.readlines()

        rows, columns, vehicles, rides, bonus, steps = [int(x) for x in city_data.split()]
        self.rows = rows
        self.columns = columns
        self.vehicles = vehicles
        self.rides = [self.parse_ride(x) for x in raw_rides]
        self.bonus = bonus

    @staticmethod
    def parse_ride(raw_ride):
        start_x, start_y, finish_x, finish_y, earliest_start, latest_finish = [int(x) for x in raw_ride.split()]

        return Ride(Location(start_x, start_y), Location(finish_x, finish_y), earliest_start, latest_finish)
