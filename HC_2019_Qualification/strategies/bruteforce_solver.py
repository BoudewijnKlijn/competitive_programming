from random import Random
import time

from HC_2019_Qualification.Pictures import Pictures
from HC_2019_Qualification.picture import Orientation
from HC_2019_Qualification.scorer_2019_q import Scorer2019Q
from HC_2019_Qualification.slide import Slide
from HC_2019_Qualification.slides import Slides
from HC_2019_Qualification.strategies.random_solver import RandomStrategy
from valcon.strategy import Strategy


class BruteForceStrategy(Strategy):
    def __init__(self, scorer: Scorer2019Q, start_seed=1, max_attempts=1000):
        self.scorer = scorer
        self.start_seed = start_seed
        self.max_attempts = max_attempts
        self.current_attempt = 0

    def _attempt_randomly(self, input_data: Pictures) -> (Slides, int):
        solution = RandomStrategy(self.start_seed + self.current_attempt).solve(input_data)
        scorer = Scorer2019Q(input_data)
        return solution, scorer.calculate(solution)

    def solve(self, input_data: Pictures) -> Slides:
        start_time = time.time()
        best_solution_score = 0
        best_solution_slides = None
        for i in range(0, self.max_attempts):
            current_solution, current_score = self._attempt_randomly(input_data)
            if current_score > best_solution_score:
                best_solution_score = current_score
                best_solution_slides = current_solution
                print(f"Improved model at iteration: {i}, current best score: {best_solution_score}")
            self.current_attempt += 1
        elapsed_time = time.time() - start_time
        print(f"Finished {self.max_attempts} attempts at brute forcing solution in {elapsed_time:.2f} seconds")
        return best_solution_slides
