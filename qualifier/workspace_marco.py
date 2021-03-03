import os
from datetime import datetime
import random
import glob
import matplotlib.pyplot as plt

from qualifier.input_data import InputData
from qualifier.output_data import OutputData
from qualifier.random_strategy import RandomStrategy
from qualifier.schedule import Schedule
from qualifier.simulatorV2.simulator_v2 import SimulatorV2
from qualifier.simulatorV4.simulator_v4 import SimulatorV4
from qualifier.strategies.AtleastOneCar import AtleastOneCar
from qualifier.strategies.BusyFirst import BusyFirst
from qualifier.strategies.BusyFirstV2 import BusyFirstV2
from qualifier.strategies.BusyFirstV3 import BusyFirstV3
from qualifier.strategies.CarsFirst import CarsFirst
from qualifier.strategies.CarsFirstBusyFirst import CarsFirstBusyFirst
from qualifier.strategies.CarsFirstShuffle import CarsFirstShuffle
from qualifier.strategies.FixedPeriods import FixedPeriods
from qualifier.strategies.RandomPeriods import RandomPeriods
from qualifier.strategies.drop_out_cars import DropOutCars
from qualifier.strategies.drop_out_specific_cars import DropOutSpecificCars
from qualifier.strategies.evolution_strategy import EvolutionStrategy
from qualifier.strategies.evolution_strategy_v2 import EvolutionStrategyV2
from qualifier.strategies.smart_random import SmartRandom
from qualifier.strategy import Strategy
from qualifier.submit import zip_submission
from qualifier.util import save_output

THIS_PATH = os.path.abspath(os.path.dirname(__file__))


class StartFirstGreen(Strategy):
    """ Streets where cars start get green light first"""
    name = 'StartFirstGreen'

    def solve(self, input_data: InputData):
        streets_with_cars = self.streets_with_car_at_light(input_data)

        streets_where_cars_start = {car.path[0].name for car in input_data.cars}

        schedules = []

        for intersection in input_data.intersections:

            schedule = []
            streets = list(intersection.incoming_streets)
            self.random.shuffle(streets)
            for street in streets:
                if street.name in streets_where_cars_start:
                    schedule.insert(0, (street.name, 1))
                elif street.name in streets_with_cars:
                    schedule.append((street.name, 1))

            schedules.append(Schedule(intersection.index, tuple(schedule)))

        return OutputData(tuple(schedules))


def setup_evolution_strategy(file_name: str):
    file_filter = {
        'a.txt': 'ignore',
        'b.txt': 'b_*.out',
        'c.txt': 'c_*.out',
        'd.txt': 'd_*.out',
        'e.txt': 'e_*.out',
        'f.txt': 'f_*.out'
    }
    saved_results = glob.glob(os.path.join(THIS_PATH, 'saved_results', file_filter[file_name]))

    parents = []

    print(f'Loading good parents: {saved_results}')
    for output_file in saved_results:
        parent = OutputData.read(output_file, input_data)
        parents.append(parent)

    # setup initial gene pool, learning from previous results and adding some from different strategies
    parents = [
        *parents,
        StartFirstGreen(seed=random.randint(0, 1_000_000)).solve(input_data),
        BusyFirst(seed=random.randint(0, 1_000_000)).solve(input_data),
        CarsFirst(seed=random.randint(0, 1_000_000)).solve(input_data),
        StartFirstGreen(seed=random.randint(0, 1_000_000)).solve(input_data),
        BusyFirstV2(seed=random.randint(0, 1_000_000)).solve(input_data),
        # BusyFirstV3(seed=random.randint(0, 1_000_000)).solve(input_data),
        SmartRandom(seed=random.randint(0, 1_000_000), ratio_permanent_red=0, max_duration=3).solve(input_data),
        RandomPeriods(seed=random.randint(0, 1_000_000), max_period=input_data.duration).solve(input_data)

        # CarsFirstBusyFirst(seed=random.randint(0, 1_000_000)).solve(input_data), # bad results atm
    ]

    evo_strategy = EvolutionStrategyV2(
        input_data=input_data,
        seed=random.randint(0, 1_000_000),
        # debug
        generations=20,
        children_per_couple=10,
        generation_size_limit=6,

        # Problem D
        # generations=20,
        # children_per_couple=10,
        # generation_size_limit=8,

        # normal
        # generations=5,
        # children_per_couple=40,
        # generation_size_limit=10,

        # bit arbitrary but scale it with the problem size
        extra_mutations=input_data.n_intersections // 5,
        gene_pool=parents,
        verbose=2,
        simulator_class=SimulatorV4,
        jobs=4
    )
    return evo_strategy


if __name__ == '__main__':

    directory = os.path.join(THIS_PATH, 'inputs')
    for file_name in [
        # 'a.txt',  # instant

        # ordered by speed (as measured by V1 simulator back in the day)

        'e.txt',  # instant
        # 'f.txt',  # 4s
        'c.txt',  # 17s
        'b.txt',  # 26s
        'd.txt',  # 2m09s

    ]:
        print(f'----- Solving {file_name} -----')
        start_time = datetime.now()
        input_data = InputData(os.path.join(directory, file_name))

        # my_strategy = StartFirstGreen(seed=random.randint(0, 1_000_000))
        # my_strategy = RandomStrategy(StartFirstGreen, seed=random.randint(0, 1_000_000), tries=10)
        my_strategy = setup_evolution_strategy(file_name)

        print(f'Solving with strategy {my_strategy.name}...')
        output = my_strategy.solve(input_data)

        print(f'Running solution trough simulator...')
        score = SimulatorV4(input_data, verbose=0).run(output)

        # print(f'---- {file_name} ----')
        # print(f'Org sim score: {Simulator(input_data, verbose=0).run(output)}')
        # print(f'V2 sim score: {score}')
        # print(f'V4 sim score: {SimulatorV4(input_data).run(output)}')

        duration = datetime.now() - start_time

        potential_score = input_data.n_cars * (input_data.duration + input_data.bonus)

        print(f"""
---------- {file_name} ---------- ({duration.seconds} seconds)
Score:  {score}         (Still to gain ~{potential_score - score} points)
                                   Bonus value: {input_data.bonus} cars: {input_data.n_cars} duration: {input_data.duration} *theoretic max: {input_data.n_cars * input_data.bonus} + {input_data.n_cars * input_data.duration} =  {potential_score}
----------------------------------------------------------
        """)

        save_output(output, file_name, score, f'M_and_B-{my_strategy.name}')

        history = my_strategy.get_history()
        if history:
            transposed = list(map(list, zip(*history)))
            x = list(range(1, len(transposed[0]) + 1))

            fig, axs = plt.subplots(2, figsize=(15, 20))

            axs[0].plot(x, transposed[0], label='Best in each generation')
            for i in range(1, len(transposed)):
                axs[0].plot(x, transposed[i], color='lightgray')

            axs[0].plot(x, transposed[-1], label='Worst in each generation')
            axs[0].set_xlabel('generation')
            axs[0].set_ylabel('score')
            axs[0].legend()
            axs[0].set_title(f'Full history: {len(x)} generations')

            axs[1].plot(x[-3:], transposed[0][-3:], label='Best in each generation')
            for i in range(1, len(transposed)):
                axs[1].plot(x[-3:], transposed[i][-3:], color='lightgray')

            axs[1].plot(x[-3:], transposed[-1][-3:], label='Worst in each generation')
            axs[1].set_xlabel('generation')
            axs[1].set_ylabel('score')
            axs[1].legend()
            axs[1].set_title(f'last 3 generations')
            fig.suptitle(f'Problem: {file_name} Strategy: {my_strategy.name} score: {score}')
            fig.show()
            fig.savefig(os.path.join(THIS_PATH, 'outputs', 'history', f'{file_name}.{score}.png'))

    zip_submission()
