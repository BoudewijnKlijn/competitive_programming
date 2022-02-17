import math

from HC_2018_Qualification.car_schedules import CarSchedule, CarSchedules
from HC_2018_Qualification.city_data import CityData
from valcon.strategies.strategy import Strategy


class BaseLineStrategy(Strategy):
    def solve(self, city_data: CityData) -> CarSchedules:
        """
        Uses a BaseLine strategy that just schedules one ride per vehicle
            or multiple if we have more rides than vehicles)
        """
        max_rides = len(city_data.rides)
        max_vehicles = city_data.vehicles

        # If more rides than vehicles, we need multiple rides per vehicle
        if max_vehicles < max_rides:
            nr_rides_per_vehicle = math.ceil(max_vehicles / max_rides)
        else:
            nr_rides_per_vehicle = 1

        # For every vehicle, just assign the nr of rides in the order we received them
        car_schedules = []
        for vehicle_idx in range(0, max_vehicles):
            current_ride_ix = vehicle_idx * nr_rides_per_vehicle
            if current_ride_ix > max_rides:
                print("All rides scheduled..")
                break

            rides = city_data.rides[current_ride_ix:current_ride_ix + nr_rides_per_vehicle]
            assert len(rides) == nr_rides_per_vehicle, f"Expected {nr_rides_per_vehicle} rides, received {len(rides)}"
            nr_rides = len(rides)

            relevant_ride_idxs = [ride.id for ride in rides]
            print(relevant_ride_idxs)
            car_schedules.append(CarSchedule(nr_rides, relevant_ride_idxs))

        output_data = CarSchedules(car_schedules)
        return output_data
