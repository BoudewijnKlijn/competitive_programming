import multiprocessing
from copy import deepcopy
from datetime import datetime
from typing import List, Tuple, Callable

from qualifier.input_data import InputData
from qualifier.output_data import OutputData
from qualifier.schedule import Schedule
from qualifier.strategies.smart_random import SmartRandom
from qualifier.strategy import Strategy

from multiprocessing import Pool
from tqdm import tqdm


class Solution:
    def __init__(self, schedules: Tuple[Schedule], score: int):
        if not isinstance(schedules, tuple):
            raise ValueError(f'Expected type tuple for schedules but got {type(schedules)}')

        self.score = score
        self.schedules = schedules

    def __copy__(self):
        raise Exception('Use deepcopy')


# so so ugly...
SIMULATORS = dict()


def _worker_initializer(simulator: Callable, input_data):
    global SIMULATORS  # dirty little trick

    worker_name = multiprocessing.current_process().name
    SIMULATORS[worker_name] = simulator(input_data=input_data)


def _worker_func(work):
    global SIMULATORS
    worker_name = multiprocessing.current_process().name
    return SIMULATORS[worker_name].run(work)


class EvolutionStrategy(Strategy):
    name = 'EvolutionStrategy'

    def __init__(self,
                 input_data: InputData,
                 generations: int,
                 children_per_couple: int,
                 generation_size_limit: int,
                 extra_mutations: int,
                 simulator_class: Callable,
                 gene_pool: List[OutputData] = None,
                 seed=27,
                 verbose=0,
                 jobs=1):
        """

        :param input_data:
        :param generations:
        :param children_per_couple: where total children will be generation_size_limit / 2 * children_per_couple
        :param generation_size_limit: the x best children will for the next generation.
        :param extra_mutations:
        :param simulator_class:
        :param seed:
        :param verbose:
        :param jobs:
        """

        super().__init__(seed=seed)

        self.gene_pool = gene_pool
        self.input_data = input_data
        self.jobs = jobs
        self.extra_mutations = extra_mutations
        self.generation_size_limit = generation_size_limit
        self.children_per_parent = children_per_couple
        self.generations = generations
        self.verbose = verbose
        self.simulator_class = simulator_class

        self.pool = None

        # create one for the algo as well.. switch to a worker once we got a handle on this...
        self.simulator = self.simulator_class(input_data=input_data)

        if verbose > 0:
            print(f"""Evolution strategy
Extra mutations: {extra_mutations}""")

        if self.jobs > 0:
            self.pool = Pool(self.jobs, initializer=_worker_initializer, initargs=(simulator_class, input_data))

    def solve(self, input_data: InputData):

        self.input_data = input_data

        parents = []

        if self.gene_pool:
            print('Using existing gene pool')
            parents = [Solution(genes.schedules, self.simulator.run(genes)) for genes in self.gene_pool]

        def add_solution():
            random_solution = SmartRandom(self.random.randint(0, 10000), max_duration=3,
                                          ratio_permanent_red=0.01).solve(
                input_data)
            score = self.simulator.run(random_solution)
            parents.append(Solution(random_solution.schedules, score))

        if len(parents) % 2 == 1:
            print('Odd amount in gene pool, adding a random parent')
            add_solution()

        print('Adding extra SmartRandom parents if needed to fill to generation_size_limit')
        for _ in range(max(0, self.generation_size_limit - len(parents))):
            add_solution()

        # working with a best score because we still have an issue with mutability.
        best_solution = deepcopy(parents[0])

        print(f'Parents: {[x.score for x in parents]}')

        current_generation = parents

        if self.verbose == 1:
            generation_iterator = tqdm(range(1, self.generations + 1))
        else:
            generation_iterator = range(1, self.generations + 1)

        for generation in generation_iterator:
            new_generation = self.create_generation(
                current_generation,
                children_per_parent=self.children_per_parent)

            current_generation += new_generation
            current_generation.sort(key=lambda solution: solution.score, reverse=True)
            current_generation = current_generation[:self.generation_size_limit]

            if self.verbose == 2:
                print(f'Generation {generation:03}/{self.generations:03}: {[p.score for p in current_generation]}')

            if current_generation[0].score > best_solution.score:
                best_solution = deepcopy(current_generation[0])
                OutputData(current_generation[0].schedules).save(
                    f'./outputs/Evo {current_generation[0].score} {datetime.now():%H%M%S}.out')

        print(f'Valid: {best_solution.score}')

        self.pool.close()
        return OutputData(best_solution.schedules)

    def _rnd_index(self, a_list):
        return self.random.randint(0, len(a_list) - 1)

    def _mutate(self, schedules: List[Schedule]) -> List[Schedule]:

        def add_duration(intersection, street, value):
            old_street = schedules[intersection].street_duration_tuples[street]
            new_value = old_street[1] + value
            new_value = min(self.input_data.duration,
                            max(0, new_value))  # max(0 untested but should work... might help in F)
            as_list = list(schedules[intersection].street_duration_tuples)
            as_list[street] = (old_street[0], new_value)
            schedules[intersection].street_duration_tuples = tuple(as_list)

        def get_rnd_street():
            intersection = self._rnd_index(schedules)
            if len(schedules[intersection].street_duration_tuples) == 0:
                # if by rng we picked an intersection with no schedule just skip it.
                print('Warning: chose an intersection without a schedule')
                return None
            street = self._rnd_index(schedules[intersection].street_duration_tuples)
            return intersection, street

        trait = self.random.randint(0, 2)
        if trait == 0:
            if location := get_rnd_street():
                if self.random.random() < 0.01:
                    # with a small percentage chance just turn this traffic light off
                    add_duration(location[0], location[1], 0)
                else:
                    add_duration(location[0], location[1], 1)
        elif trait == 1:
            if location := get_rnd_street():
                add_duration(location[0], location[1], -1)
        elif trait == 2:
            intersection = self._rnd_index(schedules)
            as_list = list(schedules[intersection].street_duration_tuples)
            self.random.shuffle(as_list)
            schedules[intersection].street_duration_tuples = tuple(as_list)
        else:
            raise ValueError('Woeps dont know what to mutate')

        return schedules

    def create_generation(self, current_generation, children_per_parent):
        children = []

        # random pair up parents
        # using shuffle to implement random sample without return
        self.random.shuffle(current_generation)
        couples = [current_generation[x:x + 2] for x in range(0, len(current_generation), 2)]

        # random select intersections of each to create children
        for parent_alice, parent_bob in couples:
            for _ in range(children_per_parent):
                # mutability starts there by copies of each parent
                alice = deepcopy(parent_alice).schedules
                child_of_bob_and_alice = list(deepcopy(parent_bob).schedules)  # makes a copy of the tuple

                gene_count = len(alice)
                gene_indexes = list(range(gene_count))

                alice_genes = self.random.sample(gene_indexes, gene_count // 2)
                for gene in alice_genes:
                    child_of_bob_and_alice[gene] = alice[gene]

                # add random mutations
                # for _ in range(self.extra_mutations):
                #     child_of_bob_and_alice = self._mutate(child_of_bob_and_alice)

                # mutability ends here by converting it to a tuple of tuples....
                children.append(tuple(child_of_bob_and_alice))

        # score children

        if self.jobs == 1:
            new_solutions = []
            for child in children:
                new_solutions.append(
                    Solution(
                        child,
                        self.simulator.run(OutputData(child))))
        else:
            outputs = [OutputData(child) for child in children]

            scores = self.pool.map(_worker_func, outputs)
            new_solutions = [Solution(child, score) for child, score in zip(children, scores)]

        return new_solutions
