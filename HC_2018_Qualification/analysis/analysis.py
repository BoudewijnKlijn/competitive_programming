import os

import numpy as np
import pandas as pd

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

    # wat is ritlengte
    # waar worden mensen vaak opgehaald en gedropt

    for problem_file in files:
        input_data = CityData(os.path.join(directory, problem_file))

        ride_distances = []
        for ride_id in input_data.rides:
            ride_distance = get_distance(ride_id.start, ride_id.end)
            ride_distances.append(ride_distance)

        theoretical_max_score = len(input_data.rides) * input_data.bonus + sum(ride_distances)

        print(f'{problem_file}')
        # print(np.array(ride_distances).mean())
        print(f'{input_data.steps=}')
        print(f'{input_data.bonus=}')
        print(f'{theoretical_max_score=:,}')
        print()
        print(pd.Series(ride_distances).describe())
        print()

