import time
import os
from collections import defaultdict
import numpy as np

from qualifier.calculate_score import calculate_score
from qualifier.input_data import InputData
from qualifier.output_data import OutputData
from qualifier.random_strategy import RandomStrategy
from qualifier.schedule import Schedule
from qualifier.strategies.BusyFirst import BusyFirst
from qualifier.strategies.BusyFirstV2 import BusyFirstV2
from qualifier.strategies.BusyFirstV3 import BusyFirstV3
from qualifier.strategy import Strategy
from qualifier.strategies.RandomPeriods import RandomPeriods
from qualifier.strategies.FixedPeriods import FixedPeriods
from qualifier.util import save_output
from qualifier.simulatorV4.simulator_v4 import SimulatorV4
from qualifier.simulatorV2.simulator_v2 import SimulatorV2
from qualifier.simulator.simulator import Simulator
from qualifier.workspace_marco import StartFirstGreen

THIS_PATH = os.path.realpath(__file__)

if __name__ == '__main__':

    directory = os.path.join('inputs')
    single_file = 'e.txt'  # file_name or None
    for file_name in os.listdir(directory):
        if single_file is not None:
            file_name = single_file
        input_data = InputData(os.path.join(directory, file_name))

        my_strategy = RandomStrategy(BusyFirstV3, SimulatorV4)  # FixedPeriods()

        output = my_strategy.solve(input_data)

        sims = [SimulatorV2, SimulatorV4]  # Simulator, SimulatorV2,
        for sim in sims:
            simulator = sim(input_data, verbose=0)
            score = simulator.run(output)
            print(f'{sim.__name__=}, {score=}')
            save_output(output, file_name, score, f'b_and_m-{sim.__name__}')

        if single_file is not None:
            break
