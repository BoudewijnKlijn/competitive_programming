import os
from datetime import datetime
import random

from qualifier.input_data import InputData
from qualifier.output_data import OutputData
from qualifier.simulatorV2.simulator_v2 import SimulatorV2
from qualifier.strategies.BusyFirst import BusyFirst
from qualifier.strategies.BusyFirstV2 import BusyFirstV2
from qualifier.strategies.BusyFirstV3 import BusyFirstV3
from qualifier.strategies.FixedPeriods import FixedPeriods
from qualifier.strategies.evolution_strategy import EvolutionStrategy
from qualifier.strategies.smart_random import SmartRandom
from qualifier.submit import zip_submission
from qualifier.util import save_output

THIS_PATH = os.path.realpath(__file__)

if __name__ == '__main__':

    directory = os.path.join(THIS_PATH, '../inputs')
    for file_name in [
        # 'a.txt',  # instant
        # 'b.txt',  # 26s
        'c.txt',  # 17s
        # 'd.txt',  # 2m09s
        # 'e.txt',  # instant
        # 'f.txt',  # 4s
    ]:

        start_time = datetime.now()
        input_data = InputData(os.path.join(directory, file_name))

        good_results = {
            'b.txt': ['b_qualifier_marco_.out'],
            'c.txt': ['c_qualifier_marco.out'],
            'd.txt': ['d_qualifier_marco.out'],
            'e.txt': ['e_qualifier_marco.out'],
            'f.txt': [
                'f_000931074_marco-EvolutionStrategy.out',
                'f_qualifier_marco.out',
                'f_980648_EvolutionStrategy.out'
            ]
        }

        my_strategy = SmartRandom(seed=random.randint(0, 1_000_000), max_duration=10, ratio_permanent_red=0.01)

        parents = []
        if file_name in good_results:
            print(f'Loading good parents')
            for output_file in good_results[file_name]:
                file = os.path.join(THIS_PATH, f'../saved_results/{output_file}')
                parent = OutputData.read(file, input_data)
                parents.append(parent)

        parents = [
            *parents,
            BusyFirst(seed=random.randint(0, 1_000_000)).solve(input_data),
            BusyFirstV2(seed=random.randint(0, 1_000_000)).solve(input_data),
            BusyFirstV3(seed=random.randint(0, 1_000_000)).solve(input_data),
            FixedPeriods(seed=random.randint(0, 1_000_000)).solve(input_data),
            # CarsFirstBusyFirst(seed=random.randint(0, 1_000_000)).solve(input_data), # bad results atm
        ]

        # simulator = SimulatorV2(input_data, verbose=0)
        # for i, parent in enumerate(parents):
        #     print(f'{i} {simulator.run(parent)}')
        # exit(0)  # debug end

        my_strategy = EvolutionStrategy(
            input_data=input_data,
            seed=random.randint(0, 1_000_000),
            # debug
            # generations=2,
            # children_per_couple=2,
            # generation_size_limit=2,

            # normal
            generations=5,
            children_per_couple=40,
            generation_size_limit=10,

            # bit arbitrary but scale it with the problem size
            extra_mutations=input_data.n_intersections // 5,
            gene_pool=parents,
            verbose=2,
            simulator_class=SimulatorV2,
            jobs=4
        )

        output = my_strategy.solve(input_data)

        score = SimulatorV2(input_data, verbose=0).run(output)
        # score = SimulatorV4(input_data).run(output)
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

        save_output(output, file_name, score, f'marco-{my_strategy.name}')

    zip_submission()
