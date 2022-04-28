"""
Based on : https://machinelearningmastery.com/simple-genetic-algorithm-from-scratch-in-python/
"""
import time

import numpy as np
from tqdm import tqdm

from HC_2022_Warmup.perfect_pizza import PerfectPizza
from HC_2022_Warmup.pizza_demands import PizzaDemands
from HC_2022_Warmup.strategies import RandomIngredients
from valcon.scorer import Scorer
from valcon.strategies.strategy import Strategy


class GeneticStrategy(Strategy):
    def __init__(self, scorer, seed=1, max_generations=1000, population_size=2, crossover_rate=0.5,
                 mutation_rate=0.5, nr_tournament_candidates=5):
        """
        Initializes a GeneticStrategy solver

        todo: improve computational speed and score performance

        Args:
            scorer (valcon.Scorer): Scorer to calculate score of slides
            seed (int): Random seed used for generating random numbers
            max_generations (int): Maximum generations for genetic solver
            population_size (int): Population size per generation
            crossover_rate (float): Cross over rate (i.e. how much of the slides to use from parent1 and parent2)
            mutation_rate (float: Mutation rate (i.e. the probability of mutations per slide transition)
            nr_tournament_candidates (int): Number of random candidates to use in tournament selection of parents
        """
        self.scorer = scorer
        self.start_seed = seed
        self.max_generations = max_generations
        self.current_generation = 0
        self.population_size = population_size
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.nr_tournament_candidates = nr_tournament_candidates
        params = {"Max_generations": max_generations,
                  "Population_size": population_size,
                  "Cross_over_rate": crossover_rate,
                  "Mutation_rate": mutation_rate,
                  "Nr_tournament_candidates": nr_tournament_candidates}
        print(f"Initialized GeneticStrategy with params: {params}")
        super().__init__(seed)

    def _generate_initial_population(self, input_data: PizzaDemands) -> [PerfectPizza]:
        """
        Generates an initial population
        """
        return [RandomIngredients().solve(input_data) for _ in range(0, self.population_size)]

    def _select_parents(self, population: [PerfectPizza], scores: [int]):
        """
        Select parents from a population by taking a random candidate,
        then uses a tournament selection to get the best scoring candidate
        """
        # first random selection
        selection_ix = np.random.randint(len(population))
        for ix in np.random.randint(0, len(population), self.nr_tournament_candidates - 1):
            # check if better (e.g. perform a tournament)
            if scores[ix] > scores[selection_ix]:
                selection_ix = ix
        return population[selection_ix]

    def _cross_over(self, parent1: PerfectPizza, parent2: PerfectPizza) -> [PerfectPizza]:
        """
        Applies cross over to two parents by selecting

        # todo: perhaps there are other better ways to do cross over?
        """
        # children are copies of parents by default
        children1, children2 = parent1, parent2
        # check for recombination
        if np.random.rand() < self.crossover_rate:
            # select crossover point that is not on the end of the items
            pt = np.random.randint(1, len(parent1.ingredients))
            # perform crossover
            # todo: use set characteristics to improve the below two lines
            children1 = PerfectPizza(list(parent1.ingredients)[:pt] + list(parent2.ingredients)[pt:])
            children2 = PerfectPizza(list(parent2.ingredients)[:pt] + list(parent1.ingredients)[pt:])
        return [children1, children2]

    def _mutation(self, child: [str]):
        """
        Mutate items by randomly switching

        # todo: there are possibly other better ways of mutating items
        """
        for i in range(len(child.ingredients) - 1):
            current_item = list(child.ingredients)[i]
            next_item = list(child.ingredients)[i + 1]
            # check for a mutation
            if np.random.rand() < self.mutation_rate:
                # switch the items
                list(child.ingredients)[i] = next_item
                list(child.ingredients)[i + 1] = current_item

    def solve(self, input_data: PizzaDemands) -> PerfectPizza:
        """
        Solves the problem by applying a genetic solver that applies the following step:
            1. Create initial population of slide decks
            2. Iterate over generations:
                2.1 Calculate score for every candidate in population
                2.2 Check best candidate in population (and keep this in memory)
                2.3 Select parent couples by applying a tournament strategy
                2.4 Apply crossover randomly (i.e. combine items of parents two generate a child)
                2.5 Apply mutations randomly (i.e. switch items transitions of children)
                2.6 Use the generated children as new population
        """
        start_time = time.time()
        population = self._generate_initial_population(input_data)

        best_solution = None
        best_solution_score = 0
        for i in tqdm(range(0, self.max_generations)):
            scores = [self.scorer.calculate(candidate) for candidate in population]

            # check for new best solution
            new_max_score = max(scores)
            if new_max_score > best_solution_score:
                idx_new_max_score = scores.index(new_max_score)
                best_solution, best_solution_score = population[idx_new_max_score].copy(), scores[
                    idx_new_max_score]
                print(f"Improved score at generation {i} with score: {best_solution_score}")

            # select parents
            selected_parents = [self._select_parents(population, scores) for _ in range(self.population_size)]
            # create the next generation
            children = []
            for k in range(0, self.population_size, 2):
                # get selected parents in pairs
                parent1, parent2 = selected_parents[k], selected_parents[k + 1]
                # crossover and mutation
                for child in self._cross_over(parent1, parent2):
                    # mutation
                    self._mutation(child)
                    # store for next generation
                    children.append(child)

            population = children

        elapsed_time = time.time() - start_time
        print(f"Finished {self.max_generations} genetic generations in {elapsed_time:.2f} seconds, "
              f"with best score: {best_solution_score}")

        return best_solution
