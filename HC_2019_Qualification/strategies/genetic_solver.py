"""
Based on : https://machinelearningmastery.com/simple-genetic-algorithm-from-scratch-in-python/
"""
from random import Random
import time

import numpy as np
from tqdm import tqdm

from HC_2019_Qualification.Pictures import Pictures
from HC_2019_Qualification.picture import Orientation
from HC_2019_Qualification.scorer_2019_q import Scorer2019Q
from HC_2019_Qualification.slide import Slide
from HC_2019_Qualification.slides import Slides
from HC_2019_Qualification.strategies.random_solver import RandomStrategy
from valcon import OutputData
from valcon.strategy import Strategy


class GeneticStrategy(Strategy):
    def __init__(self, scorer: Scorer2019Q, start_seed=1, max_generations=1000, population_size=2, crossover_rate=0.5,
                 mutation_rate=0.5):
        self.scorer = scorer
        self.start_seed = start_seed
        self.max_generations = max_generations
        self.current_generation = 0
        self.population_size = population_size
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate

    def _get_initial_population(self, input_data: Pictures):
        return [RandomStrategy(self.start_seed + self.current_generation).solve(input_data) for _ in
                range(0, self.population_size)]

    @staticmethod
    def _select_parents(population, scores, k=3):
        # first random selection
        selection_ix = np.random.randint(len(population))
        for ix in np.random.randint(0, len(population), k - 1):
            # check if better (e.g. perform a tournament)
            if scores[ix] > scores[selection_ix]:
                selection_ix = ix
        return population[selection_ix]

    def cross_over(self, parent1, parent2):
        # children are copies of parents by default
        children1, children2 = parent1, parent2
        # check for recombination
        if np.random.rand() < self.crossover_rate:
            # select crossover point that is not on the end of the string
            pt = np.random.randint(1, len(parent1.slides) - 2)
            # perform crossover
            children1 = Slides(parent1.slides[:pt] + parent2.slides[pt:])
            c2 = Slides(parent2.slides[:pt] + parent1.slides[pt:])
        return [children1, children2]

    def mutation(self, child):
        """Randomly switch two consecutive slides"""
        for i in range(len(child.slides) - 1):
            current_slide = child.slides[i]
            next_slide = child.slides[i + 1]
            # check for a mutation
            if np.random.rand() < self.mutation_rate:
                # switch the slides
                child.slides[i] = next_slide
                child.slides[i + 1] = current_slide

    def solve(self, input_data: Pictures) -> Slides:
        start_time = time.time()
        scorer = Scorer2019Q(input_data)
        population = self._get_initial_population(input_data)

        best_solution_score = 0
        best_solution_slides = None
        for i in tqdm(range(0, self.max_generations)):
            scores = [scorer.calculate(candidate) for candidate in population]

            # check for new best solution
            new_max_score = max(scores)
            if new_max_score > best_solution_score:
                idx_new_max_score = scores.index(new_max_score)
                best_solution_slides, best_solution_score = population[idx_new_max_score], scores[idx_new_max_score]
                print(f"Improved model at generation: {i}, current best score: {best_solution_score}")

            # select parents
            selected_parents = [self._select_parents(population, scores) for _ in range(self.population_size)]
            # create the next generation
            children = []
            for k in range(0, self.population_size, 2):
                # get selected parents in pairs
                parent1, parent2 = selected_parents[k], selected_parents[k + 1]
                # crossover and mutation
                for child in self.cross_over(parent1, parent2):
                    # mutation
                    self.mutation(child)
                    # store for next generation
                    children.append(child)

            # replace population
            population = children

        elapsed_time = time.time() - start_time
        print(f"Finished {self.max_generations} genetic generations in {elapsed_time:.2f} seconds")
        return best_solution_slides
