import time
import os
from collections import defaultdict
from datetime import datetime

import numpy as np

from qualifier.calculate_score import calculate_score
from qualifier.input_data import InputData
from qualifier.output_data import OutputData
from qualifier.random_strategy import RandomStrategy
from qualifier.schedule import Schedule
from qualifier.strategies.BusyFirst import BusyFirst
from qualifier.strategies.BusyFirstV2 import BusyFirstV2
from qualifier.strategies.BusyFirstV3 import BusyFirstV3
from qualifier.strategies.CarsFirstShuffle import CarsFirstShuffle
from qualifier.strategies.smart_random import SmartRandom
from qualifier.strategy import Strategy
from qualifier.strategies.RandomPeriods import RandomPeriods
from qualifier.strategies.FixedPeriods import FixedPeriods
from qualifier.util import save_output
from qualifier.simulatorV4.simulator_v4 import SimulatorV4
from qualifier.simulatorV2.simulator_v2 import SimulatorV2
from qualifier.simulator.simulatorv1 import SimulatorV1
from qualifier.workspace_marco import StartFirstGreen

THIS_PATH = os.path.realpath(__file__)

if __name__ == '__main__':

    directory = os.path.join('inputs')
    single_file = 'd.txt'  # file_name or None
    for file_name in os.listdir(directory):
        if single_file is not None:
            file_name = single_file
        input_data = InputData(os.path.join(directory, file_name))

        start = datetime.now()
        my_strategy = RandomStrategy(CarsFirstShuffle, SimulatorV4, tries=10)  # FixedPeriods()
        output = my_strategy.solve(input_data)
        elapsed = datetime.now() - start

        print(f'random 10 times, total {elapsed.seconds:0.01f} per iteration {elapsed.seconds / 10:0.01f}')

        sims = [SimulatorV2, SimulatorV4]  # Simulator, SimulatorV2,
        for sim in sims:
            simulator = sim(input_data, verbose=0)
            score, _ = simulator.run(output)
            print(f'{sim.__name__=}, {score=}')
            save_output(output, file_name, score, f'b_and_m-{sim.__name__}')

        if single_file is not None:
            break
