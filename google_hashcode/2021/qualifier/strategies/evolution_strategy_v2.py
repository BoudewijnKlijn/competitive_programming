import multiprocessing
from copy import deepcopy
from datetime import datetime
from typing import List, Tuple, Callable

from qualifier.input_data import InputData
from qualifier.output_data import OutputData
from qualifier.schedule import Schedule, EvaluatedSchedule
from qualifier.strategies.smart_random import SmartRandom
from qualifier.strategy import Strategy

from multiprocessing import Pool
from tqdm import tqdm
import numpy as np

# to catch runtime warnings
np.seterr(all='raise')


class Solution:
    def __init__(self, schedules: Tuple[Schedule], score: int):
        if not isinstance(schedules, tuple):
            raise ValueError(f'Expected type tuple for schedules but got {type(schedules)}')

        if not isinstance(score, int):
            raise ValueError(f'Expected score to be of type int got {type(score)}')

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


class EvolutionStrategyV2(Strategy):
    name = 'EvolutionStrategy'

    # TODO: swithc to MultiCoreStrategy class
    # TODO: drop duplicate genomes (prefer lowerscoring genomes instead to keep diversity)

    def __init__(self,
                 input_data: InputData,
                 generations: int,
                 children_per_couple: int,
                 generation_size_limit: int,
                 extra_mutations: int,
                 simulator_class: Callable,
                 children_strategies: Strategy,
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
        self.children_strategies = children_strategies
        self.history = []
        self.pool = None

        # create one for the algo as well.. switch to a worker once we got a handle on this...
        self.simulator = self.simulator_class(input_data=input_data)

        if verbose > 0:
            print(f""" --- Evolution strategy ---
Genes: {input_data.n_intersections}
Extra mutations: {extra_mutations} ({extra_mutations / input_data.n_intersections * 100:0.01f}%)""")

        if self.jobs > 0:
            self.pool = Pool(self.jobs, initializer=_worker_initializer, initargs=(simulator_class, input_data))

    def solve(self, input_data: InputData):

        self.input_data = input_data

        starting_solutions = []

        if self.gene_pool:
            print('Using existing gene pool')
            starting_solutions += self.gene_pool

        def add_solution():
            random_solution = self.children_strategies(self.random.randint(0, 10000)).solve(input_data)
            starting_solutions.append(random_solution)

        if len(starting_solutions) % 2 == 1:
            print('Odd amount in gene pool, adding a random parent')
            add_solution()

        print(f'Adding extra {self.children_strategies.name} parents if needed to fill to generation_size_limit')
        for _ in range(max(0, self.generation_size_limit - len(starting_solutions))):
            add_solution()

        simulation_results = self.pool.map(_worker_func, starting_solutions)
        parents = [Solution(output.schedules, score) for score, output in simulation_results]

        # easier to compare to first generation
        parents.sort(key=lambda solution: solution.score, reverse=True)

        # working with a best score because we still have an issue with mutability.
        best_solution = deepcopy(parents[0])

        # extra spaces to align with generations output
        print(f'Parents           : {[x.score for x in parents]}')

        current_generation = parents

        if self.verbose == 1:
            generation_iterator = tqdm(range(1, self.generations + 1))
        else:
            generation_iterator = range(1, self.generations + 1)

        start = datetime.now()
        for generation in generation_iterator:
            current = datetime.now()
            new_generation = self.create_generation(
                current_generation,
                children_per_parent=self.children_per_parent)

            # consider giving genes that survived a generation a tiny bonus survival
            # consider keeping a few genomes that are novel so to maintain diversity
            #  - perhaps generating hash codes of genes and counting nr of unique genes a genome has

            current_generation += new_generation
            current_generation.sort(key=lambda solution: solution.score, reverse=True)
            current_generation = current_generation[:self.generation_size_limit]

            scores = [p.score for p in current_generation]

            if self.verbose == 2:
                elapsed = datetime.now() - current
                total_elapsed = datetime.now() - start
                estimated_duration = total_elapsed / generation * (self.generations + 1)

                print(
                    f'Generation {generation:03}/{self.generations:03}: {scores}  [{elapsed.seconds}s| {start + estimated_duration:%H:%M}]')

            self.history.append(scores)

            if current_generation[0].score > best_solution.score:
                best_solution = deepcopy(current_generation[0])
            for child in current_generation:
                OutputData(child.schedules).save(
                    f'./outputs/intermediate results/_{child.score:09}_Evo.out')

        print(f'Valid: {best_solution.score}')

        self.pool.close()
        return OutputData(best_solution.schedules)

    def _rnd_index(self, a_list):
        return self.random.randint(0, len(a_list) - 1)

    def _mutate(self, schedules: List[EvaluatedSchedule], losses) -> List[Schedule]:

        def get_weighted_random_intersection(schedules, losses):
            """ returns the index of a random street, with a higher probability for intersections with long wait times"""
            total_loss = sum(losses)
            rnd = self.random.randint(1, total_loss)
            for index, schedule in enumerate(schedules):
                rnd -= losses[index]
                if rnd <= 0:
                    return index

        def add_duration(intersection, street, value):
            old_street = schedules[intersection].street_duration_tuples[street]
            new_value = old_street[1] + value
            new_value = min(self.input_data.duration,
                            max(0, new_value))  # max(0 untested but should work... might help in F)
            as_list = list(schedules[intersection].street_duration_tuples)
            as_list[street] = (old_street[0], new_value)
            schedules[intersection].street_duration_tuples = tuple(as_list)

        # def random_duration(intersection, street):
        #     old_street = schedules[intersection].street_duration_tuples[street]
        #     new_value = self.random.randint(1, 3)
        #     as_list = list(schedules[intersection].street_duration_tuples)
        #     as_list[street] = (old_street[0], new_value)
        #     schedules[intersection].street_duration_tuples = tuple(as_list)

        def get_rnd_street():
            # we could also weight individual streets.. but due to the interplay it might actualy be bad to do so
            intersection = get_weighted_random_intersection(schedules, losses)
            if len(schedules[intersection].street_duration_tuples) == 0:
                # if by rng we picked an intersection with no schedule just skip it.
                print('Warning: chose an intersection without a schedule')
                return None
            street = self._rnd_index(schedules[intersection].street_duration_tuples)
            return intersection, street

        trait = self.random.randint(0, 2)
        if trait == 0:  # add 1 second to a green light duration
            if location := get_rnd_street():
                add_duration(location[0], location[1], 1)
        elif trait == 1:  # remove 1 second from a green light duration
            if location := get_rnd_street():
                add_duration(location[0], location[1], -1)
        elif trait == 2:  # move the order of 1 streets green light up or down 1 step
            intersection = self._rnd_index(schedules)
            as_list = list(schedules[intersection].street_duration_tuples)
            street_count = len(as_list)
            if street_count > 1:  # no need to do stuff with 0 or 1 streets..
                random_str = self.random.randint(0, street_count - 1)
                street = as_list.pop(random_str)
                up = self.random.randint(0, 1)
                if up:
                    new_index = (random_str + 1) % street_count
                else:
                    # insert at end if we go negative
                    new_index = (random_str - 1) if random_str else street_count - 1
                as_list.insert(new_index, street)

                schedules[intersection].street_duration_tuples = tuple(as_list)
        else:
            raise ValueError(f'Woeps dont know what to mutate')

        return schedules

    def get_history(self):
        return self.history

    @staticmethod
    def softmax(alice_loss, bob_loss):
        """Calculates 1 - softmax """
        loss = np.array([alice_loss, bob_loss])
        norm = np.linalg.norm(loss)
        normalized_loss = loss / (norm if norm else 1)  # avoid div by 0
        softmax = np.exp(normalized_loss) / sum(np.exp(normalized_loss))
        return softmax

    @staticmethod
    def schedule_loss(schedule):
        return sum([street[2] for street in schedule.street_duration_tuples])

    @staticmethod
    def gene_weight_alice(alice_gene: EvaluatedSchedule, bob_gene: EvaluatedSchedule):
        bob_loss = EvolutionStrategyV2.schedule_loss(bob_gene)
        alice_loss = EvolutionStrategyV2.schedule_loss(alice_gene)
        softmax = EvolutionStrategyV2.softmax(alice_loss, bob_loss)

        # since it was a loss, and we want only to pick alice if bob was bad
        # example: bob wait time 99 alice wait time 1
        # softmax .1 .99
        # so we want to pick alice with a probability of .99 since bob's gene was horrible
        return softmax[1]

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

                for gene_index in range(gene_count):
                    alice_gene_probability = self.gene_weight_alice(alice[gene_index],
                                                                    child_of_bob_and_alice[gene_index])
                    if self.random.random() < alice_gene_probability:
                        child_of_bob_and_alice[gene_index] = alice[gene_index]

                losses = [self.schedule_loss(gene) for gene in child_of_bob_and_alice]

                # add random mutations
                for _ in range(self.extra_mutations):
                    child_of_bob_and_alice = self._mutate(child_of_bob_and_alice, losses)

                # mutability ends here by converting it to a tuple of tuples....
                children.append(tuple(child_of_bob_and_alice))

        # score children

        if self.jobs == 1:
            new_solutions = []
            for child in children:
                score, output = self.simulator.run(OutputData(child))
                new_solutions.append(
                    Solution(output.schedules, score))
        else:
            outputs = [OutputData(child) for child in children]

            simulation_results = self.pool.map(_worker_func, outputs)
            new_solutions = [Solution(output.schedules, score) for score, output in simulation_results]

        return new_solutions
