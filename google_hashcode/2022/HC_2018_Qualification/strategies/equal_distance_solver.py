import math
from copy import deepcopy

import numpy as np

from HC_2018_Qualification.car_schedules import CarSchedule, CarSchedules
from HC_2018_Qualification.city_data import CityData
from valcon.strategies.strategy import Strategy


class EqualDistanceSolver(Strategy):
    def solve(self, city_data: CityData) -> CarSchedules:
        """
        Assign every vehicle (circa) the same distance
        """
        max_rides = len(city_data.rides)
        max_vehicles = city_data.vehicles

        # If more rides than vehicles, we need multiple rides per vehicle
        if max_vehicles < max_rides:
            nr_rides_per_vehicle = math.ceil(max_rides / max_vehicles)
        else:
            nr_rides_per_vehicle = 1

        distances = [ride.max_payout for ride in city_data.rides]
        # distances = sorted(distances)
        avg_distance = math.ceil(np.mean(distances))

        car_schedules = []
        city_data_rides = deepcopy(city_data.rides)
        for vehicle_idx in range(0, max_vehicles):
            rides = self._get_rides(city_data_rides, avg_distance)
            nr_rides = len(rides)
            relevant_ride_idxs = [ride.id for ride in rides]
            car_schedules.append(CarSchedule(nr_rides, relevant_ride_idxs))

        output_data = CarSchedules(car_schedules)
        return output_data

    @staticmethod
    def _get_rides(city_data_rides, total_distance):
        curr_distance = 0
        rides = []
        tmp_city_data_rides = deepcopy(city_data_rides)
        for i in range(0, len(tmp_city_data_rides)):
            curr_ride = tmp_city_data_rides[i]
            rides.append(curr_ride)
            city_data_rides.remove(curr_ride)
            curr_distance += curr_ride.max_payout
            if curr_distance >= total_distance:
                break
        return rides
