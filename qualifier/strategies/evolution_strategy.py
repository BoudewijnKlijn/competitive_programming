from typing import List, Tuple

from qualifier.input_data import InputData
from qualifier.output_data import OutputData
from qualifier.schedule import Schedule
from qualifier.simulator.simulator import Simulator
from qualifier.strategies.smart_random import SmartRandom
from qualifier.strategy import Strategy

from multiprocessing import Pool
from tqdm import tqdm


class Solution:
    def __init__(self, schedules: Tuple[Schedule], score: int):
        self.score = score
        self.schedules = schedules
        self.score_id = id(score)
        self.schedules_id = id(self.schedules)

    def valid(self):
        """ check if not modified """
        return self.score_id == id(self.score) and \
               self.schedules_id == id(self.schedules)


class EvolutionStrategy(Strategy):
    name = 'EvolutionStrategy'

    def __init__(self, generations: int, children_per_couple: int, survivor_count: int, extra_mutations: int, seed=27,
                 verbose=0):
        super().__init__(seed=seed)
        self.extra_mutations = extra_mutations
        self.survivor_count = survivor_count
        self.children_per_parent = children_per_couple
        self.generations = generations
        self.input_data = None
        self.verbose = verbose

    def solve(self, input_data: InputData):
        self.input_data = input_data
        parents = []
        for _ in range(2):
            random_solution = SmartRandom(self.random.randint(0, 100), max_duration=3).solve(input_data)
            score = Simulator(input_data=self.input_data).run(random_solution)
            parents.append(Solution(random_solution.schedules, score))

        current_generation = parents

        if self.verbose == 1:
            generation_iterator = tqdm(range(1, self.generations + 1))
        else:
            generation_iterator = range(1, self.generations + 1)

        for generation in generation_iterator:
            new_generation = self.create_generation(
                current_generation,
                children_per_parent=self.children_per_parent)
            #
            # for sol in new_generation:
            #     print(Simulator(input_data=self.input_data, output_data=sol.output).run())

            current_generation += new_generation
            current_generation.sort(key=lambda solution: solution.score, reverse=True)
            current_generation = current_generation[:self.survivor_count]

            if self.verbose == 2:
                print(f'Generation {generation:03}/{self.generations:03}: {current_generation[0].score}')
            # print(f'scores: {[x.score for x in current_generation]}')

        if not current_generation[0].valid():
            raise ValueError('Somebody mutated me!')
        else:
            print(f'Valid: {current_generation[0].score} {type(current_generation[0].schedules)}')

        return OutputData(current_generation[0].schedules)

    def _rnd_index(self, a_list):
        return self.random.randint(0, len(a_list) - 1)

    def _mutate(self, schedules: List[Schedule]) -> Tuple[Schedule]:

        schedules = list(schedules)  # I have a bug somewhere... this is inefficient...

        def add_duration(intersection, street, value):
            schedules[intersection] = schedules[intersection].copy()
            old_street = schedules[intersection].street_duration_tuples[street]
            new_value = old_street[1] + value
            new_value = min(self.input_data.duration,
                            max(0, new_value))  # max(0 untested but should work... might help in F)
            schedules[intersection].street_duration_tuples[street] = (old_street[0], new_value)

        def get_rnd_street():
            intersection = self._rnd_index(schedules)
            if len(schedules[intersection].street_duration_tuples) == 0:
                return None
            street = self._rnd_index(schedules[intersection].street_duration_tuples)
            return (intersection, street)

        trait = self.random.randint(0, 2)
        if trait == 0:
            if location := get_rnd_street():
                add_duration(location[0], location[1], 1)
        elif trait == 1:
            if location := get_rnd_street():
                add_duration(location[0], location[1], -1)
        elif trait == 2:
            intersection = self._rnd_index(schedules)
            self.random.shuffle(schedules[intersection].street_duration_tuples)
        else:
            raise ValueError(f'Woeps dont know what to mutate')

        return tuple(schedules)

    @staticmethod
    def _clone_schedules(schedules: Tuple[Schedule]):
        return tuple([schedule.copy() for schedule in schedules])

    def create_generation(self, current_generation, children_per_parent):
        children = []

        # random pair up parents
        # using shuffle to implement random sample without return
        self.random.shuffle(current_generation)
        couples = [current_generation[x:x + 2] for x in range(0, len(current_generation), 2)]

        # random select intersections of each to create children
        for parent_alice, parent_bob in couples:
            alice = self._clone_schedules(parent_alice.schedules)  # searching for the bug

            gene_count = len(alice)
            gene_indexes = list(range(gene_count))
            for _ in range(children_per_parent):
                child_of_bob_and_alice = list(self._clone_schedules(parent_bob.schedules))  # makes a copy of the tuple
                alice_genes = self.random.sample(gene_indexes, gene_count // 2)
                for gene in alice_genes:
                    child_of_bob_and_alice[gene] = alice[gene]

                # add random mutations
                for _ in range(self.extra_mutations):
                    child_of_bob_and_alice = self._mutate(child_of_bob_and_alice)
                children.append(tuple(child_of_bob_and_alice))

        # score children 

        # Bug max recursion depth with pickling objects.... (but does work on a.in)
        # simulator = Simulator(input_data=self.input_data)
        # outputs = [OutputData(child) for child in children]
        # with Pool(8) as pool:
        #     scores = pool.map(simulator.run, outputs)
        # new_solutions = [Solution(child, score) for child, score in zip(children, scores)]

        new_solutions = []
        for child in children:
            new_solutions.append(
                Solution(
                    child,
                    Simulator(input_data=self.input_data).run(OutputData(child))))

        return new_solutions
