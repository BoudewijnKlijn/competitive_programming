import os

import pandas as pd
import matplotlib.pyplot as plt

from HC_2018_Qualification.city_data import CityData
from HC_2018_Qualification.ride_scorer import get_distance

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

    # waar worden mensen vaak opgehaald en gedropt
    # je wilt alleen rides pakken die dropoffs hebben in de buurt van volgende pickups

    for problem_file in files:
        input_data = CityData(os.path.join(directory, problem_file))

        ride_distances = []
        pickup_locations = []
        dropoff_locations = []
        for ride_id in input_data.rides:
            ride_distance = get_distance(ride_id.start, ride_id.end)
            ride_distances.append(ride_distance)
            pickup_locations.append(ride_id.start)
            dropoff_locations.append(ride_id.end)

        theoretical_max_score = len(input_data.rides) * input_data.bonus + sum(ride_distances)

        print(f'{problem_file}')
        print(f'{input_data.steps=}')
        print(f'{input_data.bonus=}')
        print(f'{theoretical_max_score=:,}')
        print()
        print(pd.Series(ride_distances).describe())
        print()

        for name, locations in [('pickups', pickup_locations), ('dropoffs', dropoff_locations)]:
            xs, ys = zip(*locations)
            fig, ax = plt.subplots()
            plt.scatter(xs, ys, alpha=0.5, linewidths=0)
            plt.xlim(0, input_data.columns)
            plt.ylim(0, input_data.rows)
            fig.savefig(f'{problem_file}_{name}.png')

