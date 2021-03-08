import os
from datetime import datetime
import random

from qualifier.input_data import InputData
from qualifier.strategies.PlanV2 import PlanV2
from qualifier.simulatorV5.simulator_v5 import SimulatorV5
from qualifier.strategies.Plan import Plan
from qualifier.strategies.random_strategy_multi_core import RandomStrategyMultiCore
from qualifier.util import save_output
from qualifier.simulatorV4.simulator_v4 import SimulatorV4

THIS_PATH = os.path.realpath(__file__)

if __name__ == '__main__':
    directory = os.path.join('inputs')

    single_file = 'd.txt'  # file_name or None

    for file_name in os.listdir(directory):
        if single_file is not None:
            file_name = single_file

        print(f'File: {file_name}')
        input_data = InputData(os.path.join(directory, file_name))

        seed = random.randint(1, 1_000_000)

        profile = False
        save = True
        jobs = 6
        iteration_count = jobs * 1

        strategy = PlanV2

        try:
            if profile == False:
                start = datetime.now()
                my_strategy = RandomStrategyMultiCore(strategy, SimulatorV4, tries=iteration_count,
                                                      seed=seed, jobs=jobs, input_data=input_data)  # FixedPeriods()
                _ = my_strategy.solve(input_data)
                elapsed_v4 = datetime.now() - start
                print(
                    f'V4 random {iteration_count} times, total {elapsed_v4.seconds:0.01f} per iteration {elapsed_v4.seconds / iteration_count:0.02f}')
                print('---------------------------------------------------------------')

            start = datetime.now()
            my_strategy = RandomStrategyMultiCore(strategy, SimulatorV5, tries=iteration_count, input_data=input_data,
                                                  seed=seed, jobs=jobs)  # FixedPeriods()
            output_v5 = my_strategy.solve(input_data)
            elapsed_v5 = datetime.now() - start
            print(
                f'V5 random {iteration_count} times, total {elapsed_v5.seconds:0.01f} per iteration {elapsed_v5.seconds / iteration_count:0.02f}')
            print('---------------------------------------------------------------')

            if profile == False:
                sims = [SimulatorV4, SimulatorV5]  # SimulatorV2,
                for sim in sims:
                    simulator = sim(input_data, verbose=0)
                    score, _ = simulator.run(output_v5)
                    print(f'{sim.__name__=}, {score=}')

            if save:
                score, _ = SimulatorV5(input_data, verbose=0).run(output_v5)
                save_output(output_v5, file_name, score, f'b_and_m-{my_strategy.name}')

            if single_file is not None:
                break
        finally:
            # still need to figure out better way to close mulythreaded pool
            my_strategy.__del__()
