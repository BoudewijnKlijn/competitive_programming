import math
import os
import statistics
from datetime import datetime
import random
import glob
import matplotlib.pyplot as plt

from qualifier.input_data import InputData
from qualifier.output_data import OutputData
from qualifier.simulatorV4.simulator_v4 import SimulatorV4
from qualifier.simulatorV5.simulator_v5 import SimulatorV5
from qualifier.strategies.BusyFirst import BusyFirst
from qualifier.strategies.CarsFirst import CarsFirst
from qualifier.strategies.Plan import Plan
from qualifier.strategies.PlanV2 import PlanV2
from qualifier.strategies.PlanV3 import PlanV3
from qualifier.strategies.PlanV4 import PlanV4
from qualifier.strategies.RandomPeriods import RandomPeriods
from qualifier.strategies.evolution_strategy_v2 import EvolutionStrategyV2
from qualifier.strategies.smart_random import SmartRandom
from qualifier.strategies.start_first_green import StartFirstGreen
from qualifier.submit import zip_submission
from qualifier.util import save_output

THIS_PATH = os.path.abspath(os.path.dirname(__file__))


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
        # CarsFirst(seed=random.randint(0, 1_000_000)).solve(input_data),
        # StartFirstGreen(seed=random.randint(0, 1_000_000)).solve(input_data),
        # StartFirstGreen(seed=random.randint(0, 1_000_000)).solve(input_data),
        # BusyFirst(seed=random.randint(0, 1_000_000)).solve(input_data),
        Plan(seed=random.randint(0, 1_000_000)).solve(input_data),
        PlanV2(seed=random.randint(0, 1_000_000)).solve(input_data),
        # skips intersections CarsFirst(seed=random.randint(0, 1_000_000)).solve(input_data),
        # x BusyFirstV2(seed=random.randint(0, 1_000_000)).solve(input_data),
        # x BusyFirstV3(seed=random.randint(0, 1_000_000)).solve(input_data),

        # SmartRandom(seed=random.randint(0, 1_000_000), ratio_permanent_red=0, max_duration=5).solve(input_data),
        # RandomPeriods(seed=random.randint(0, 1_000_000), max_period=input_data.duration // 2).solve(input_data)

        # x CarsFirstBusyFirst(seed=random.randint(0, 1_000_000)).solve(input_data), # bad results atm
    ]

    if file_name == 'd.txt':
        extra_mutations = max(1, input_data.n_intersections // 300)
        generation_size_limit = 60
        generations = 10
        children = 2
        children_strategies = PlanV2
    elif file_name == 'e.txt':
        extra_mutations = max(1, input_data.n_intersections // 250)
        generation_size_limit = 30
        generations = 400
        children = 2
        children_strategies = SmartRandom
    elif file_name == 'f.txt':
        extra_mutations = max(1, input_data.n_intersections // 200)
        generation_size_limit = 30
        generations = 30
        children = 2
        children_strategies = SmartRandom
    else:
        extra_mutations = max(1, input_data.n_intersections // 100)
        generation_size_limit = 30
        generations = 20
        children = 1
        children_strategies = SmartRandom

    evo_strategy = EvolutionStrategyV2(
        input_data=input_data,
        seed=random.randint(0, 1_000_000),
        generations=generations,

        # debug
        # generation_size_limit=2,
        # jobs=1,

        generation_size_limit=generation_size_limit,
        children_per_couple=children,
        children_strategies=children_strategies,
        jobs=4,

        # normal
        # generation_size_limit=10,
        # jobs=4,

        # bit arbitrary but scale it with the problem size
        extra_mutations=extra_mutations,
        gene_pool=parents,
        verbose=2,
        simulator_class=SimulatorV5,
    )
    return evo_strategy


if __name__ == '__main__':

    directory = os.path.join(THIS_PATH, 'inputs')
    for file_name in [

        # a.txt: 2002
        # b.txt: 4576202
        # c.txt: 1328389
        # d.txt: 3986591
        # e.txt: 921203
        # f.txt: 1765068

        # 'a.txt',  # instant

        # ordered by speed (as measured by V1 simulator back in the day)
        # 'e.txt',  # 920k optimal, current 730k
        # 'f.txt',  # 176k optimal, current 141k
        # 'c.txt',  # 1328389 optimal, current 1,310,996 points
        # 'b.txt',  # 4576202 optimal, current 4,568,491 points
        'd.txt',  # 3986k optimal, current 1,974,754 points

    ]:
        print(f'----- Solving {file_name} -----')
        start_time = datetime.now()
        input_data = InputData(os.path.join(directory, file_name))

        my_strategy = PlanV4(seed=random.randint(0, 1_000_000))
        # my_strategy = RandomStrategy(StartFirstGreen, seed=random.randint(0, 1_000_000), tries=10)
        # my_strategy = setup_evolution_strategy(file_name)

        print(f'Solving with strategy {my_strategy.name}...')
        output = my_strategy.solve(input_data)

        print(f'Running solution trough simulator...')
        sim = SimulatorV4(input_data, verbose=0)
        score, evaluation = sim.run(output)

        waiting_times = [sum([street[2] for street in intersection.street_duration_tuples]) for intersection in
                         evaluation.schedules]
        print(f"""Total waiting time: {sum(waiting_times)}
avg waiting time per intersection: {statistics.mean(waiting_times):0.01f}
avg waiting time per car: {sum(waiting_times) / input_data.n_cars:0.01f}
""")

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

            for i in range(1, len(transposed)):
                axs[0].plot(x, transposed[i], color='lightgray')

            axs[0].plot(x, transposed[-1], label='Worst in each generation')
            axs[0].plot(x, transposed[0], label='Best in each generation')
            axs[0].set_xlabel('generation')
            axs[0].set_ylabel('score')
            axs[0].legend()
            axs[0].set_title(f'Full history: {len(x)} generations')

            for i in range(1, len(transposed)):
                axs[1].plot(x[-3:], transposed[i][-3:], color='lightgray')

            axs[1].plot(x[-3:], transposed[-1][-3:], label='Worst in each generation')
            axs[1].plot(x[-3:], transposed[0][-3:], label='Best in each generation')
            axs[1].set_xlabel('generation')
            axs[1].set_ylabel('score')
            axs[1].legend()
            axs[1].set_title(f'last 3 generations')
            fig.suptitle(f'Problem: {file_name} Strategy: {my_strategy.name} score: {score}')
            fig.show()
            fig.savefig(os.path.join(THIS_PATH, 'outputs', 'history', f'{file_name}.{score}.png'))

    zip_submission()
