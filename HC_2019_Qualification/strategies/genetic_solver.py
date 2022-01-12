"""
Based on : https://machinelearningmastery.com/simple-genetic-algorithm-from-scratch-in-python/
"""
import time

import numpy as np
from tqdm import tqdm

from HC_2019_Qualification.Pictures import Pictures
from HC_2019_Qualification.scorer_2019_q import Scorer2019Q
from HC_2019_Qualification.slides import Slides
from HC_2019_Qualification.strategies.random_solver import RandomStrategy
from valcon.strategy import Strategy


class GeneticStrategy(Strategy):
    def __init__(self, scorer: Scorer2019Q, start_seed=1, max_generations=1000, population_size=2, crossover_rate=0.5,
                 mutation_rate=0.5, nr_tournament_candidates=5):
        """
        Initializes a GeneticStrategy solver

        todo: improve computational speed and score performance

        Args:
            scorer (HC_2019_Qualification.scorer_2019_q.Scorer2019Q): Scorer to calculate score of slides
            start_seed (int): Random seed used for generating random numbers
            max_generations (int): Maximum generations for genetic solver
            population_size (int): Population size per generation
            crossover_rate (float): Cross over rate (i.e. how much of the slides to use from parent1 and parent2)
            mutation_rate (float: Mutation rate (i.e. the probability of mutations per slide transition)
            nr_tournament_candidates (int): Number of random candidates to use in tournament selection of parents
        """
        self.scorer = scorer
        self.start_seed = start_seed
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

    def _generate_initial_population(self, input_data: Pictures) -> [Slides]:
        """
        Generates an initial population by generating Random slides (i.e. slidedecks)

        Args:
            input_data (HC_2019_Qualification.Pictures): Pictures to use for slides

        Returns:
            [HC_2019_Qualification.slides]: List of slides (i.e. list of slidedecks)
        """
        return [RandomStrategy(self.start_seed + self.current_generation).solve(input_data) for _ in
                range(0, self.population_size)]

    def _select_parents(self, population: [Slides], scores: [int]):
        """
        Select parents from a population by taking a random candidate,
        then uses a tournament selection to get the best scoring candidate

        Args:
            population ([HC_2019_Qualification.slides]): Population of Slides
            scores ([int]): List of scores belonging to population

        Returns:
            [HC_2019_Qualification.slides]: Two Slides objects
        """
        # first random selection
        selection_ix = np.random.randint(len(population))
        for ix in np.random.randint(0, len(population), self.nr_tournament_candidates - 1):
            # check if better (e.g. perform a tournament)
            if scores[ix] > scores[selection_ix]:
                selection_ix = ix
        return population[selection_ix]

    def _cross_over(self, parent1: Slides, parent2: Slides) -> [Slides]:
        """
        Applies cross over to two parents by selecting

        Args:
            parent1 (HC_2019_Qualification.slides.Slides): Parent1 slide deck
            parent2 (HC_2019_Qualification.slides.Slides): Parent2 slide deck

        Returns:
            [HC_2019_Qualification.slides.Slides]: Two children slide decks
        """
        # children are copies of parents by default
        children1, children2 = parent1, parent2
        # check for recombination
        if np.random.rand() < self.crossover_rate:
            # select crossover point that is not on the end of the slide deck
            pt = np.random.randint(1, len(parent1.slides) - 2)
            # perform crossover
            children1 = Slides(parent1.slides[:pt] + parent2.slides[pt:])
            children2 = Slides(parent2.slides[:pt] + parent1.slides[pt:])
        return [children1, children2]

    def _mutation(self, child: Slides):
        """
        Mutate slides by randomly switching two consecutive slides

        Args:
            child (HC_2019_Qualification.slides.Slides): Slide deck
        """
        for i in range(len(child.slides) - 1):
            current_slide = child.slides[i]
            next_slide = child.slides[i + 1]
            # check for a mutation
            if np.random.rand() < self.mutation_rate:
                # switch the slides
                child.slides[i] = next_slide
                child.slides[i + 1] = current_slide

    def solve(self, input_data: Pictures) -> Slides:
        """
        Solves the problem by applying a genetic solver that applies the following step:
            1. Create initial population of slide decks
            2. Iterate over generations:
                2.1 Calculate score for every candidate in population
                2.2 Check best candidate in population (and keep this in memory)
                2.3 Select parent couples by applying a tournament strategy
                2.4 Apply crossover randomly (i.e. combine slides of parents two generate a child)
                2.5 Apply mutations randomly (i.e. switch slide transitions of children)
                2.6 Use the generated children as new population

        Args:
            input_data (HC_2019_Qualification.Pictures): Pictures to use for slides

        Returns:
            HC_2019_Qualification.slides.Slides: Slide deck with solution
        """
        start_time = time.time()
        scorer = Scorer2019Q(input_data)
        population = self._generate_initial_population(input_data)

        best_solution_slides = None
        best_solution_score = 0
        for i in tqdm(range(0, self.max_generations)):
            scores = [scorer.calculate(candidate) for candidate in population]

            # check for new best solution
            new_max_score = max(scores)
            if new_max_score > best_solution_score:
                idx_new_max_score = scores.index(new_max_score)
                best_solution_slides, best_solution_score = population[idx_new_max_score].copy(), scores[
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

        return best_solution_slides
