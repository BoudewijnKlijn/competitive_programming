import multiprocessing
import os

from HC_2019_Qualification.Pictures import Pictures
from HC_2019_Qualification.scorer_2019_q import Scorer2019Q
from HC_2019_Qualification.slides import Slides
from HC_2019_Qualification.strategies.bruteforce_solver import BruteForceStrategy
from HC_2019_Qualification.strategies.genetic_solver import GeneticStrategy
from valcon import InputData
from valcon.scorer import Scorer

THIS_PATH = os.path.abspath(os.path.dirname(__file__))


def run_bruteforce_strategy():
    directory = os.path.join(THIS_PATH, 'HC_2019_Qualification', 'input')
    input_data = Pictures(os.path.join(directory, 'b_lovely_landscapes.txt'))

    scorer = Scorer2019Q(input_data)
    strategy = BruteForceStrategy(scorer)
    solution = strategy.solve(input_data)

    # todo_ fix double calculating score
    score = scorer.calculate(solution)

    print(f'Score: {score}')


if __name__ == '__main__':
    directory = os.path.join(THIS_PATH, 'HC_2019_Qualification', 'input')
    input_path = os.path.join(directory, 'c_memorable_moments.txt')
    input_data = Pictures(input_path)

    print(f"Running GeneticStrategy with input path: {input_path}")
    scorer = Scorer2019Q(input_data)
    strategy = GeneticStrategy(scorer, max_generations=100, population_size=100, mutation_rate=0.5, crossover_rate=0.5)
    solution = strategy.solve(input_data)

    score = scorer.calculate(solution)

    print(f'FINAL SCORE: {score}')

    pass
