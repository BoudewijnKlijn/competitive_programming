import json
import os
from collections import Counter

from HC_2018_Qualification.city_data import CityData
from HC_2018_Qualification.ride_scorer import RideScore

THIS_PATH = os.path.abspath(os.path.dirname(__file__))

if __name__ == '__main__':
    directory = os.path.join(THIS_PATH, '../input')
    files = [
        'a_example.in',
        'b_should_be_easy.in',
        'c_no_hurry.in',
        'd_metropolis.in',
        'e_high_bonus.in',
    ]

    # wat is ritlengte
    # waar worden mensen vaak opgehaald en gedropt

    for problem_file in files:
        input_data = CityData(os.path.join(directory, problem_file))
        scorer = RideScore(input_data)

        ride_distances = []
        for ride in input_data.rides:
            ride_distance = scorer.distance(ride.start, ride.end)
            ride_distances.append(ride_distance)

        print(mean)

