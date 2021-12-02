from random import Random

from HC_2019_Qualification.input_data_2019_q import Pictures
from HC_2019_Qualification.slides import Slides
from HC_2019_Qualification.strategies.baseline_solver import BaseLineStrategy
from valcon.strategy import Strategy
from HC_2019_Qualification.scorer_2019_q import Scorer2019Q


class RandomSortFlipStrategy(Strategy):
    def __init__(self, seed: int, n_flips: int = 1_000):
        self.seed = seed
        self.n_flips = n_flips

    def solve(self, input_data: Pictures) -> Slides:

        # Random shuffle.
        rng = Random(self.seed)
        rng.shuffle(input_data.pictures)

        # Sort by number of tags.
        input_data.pictures = sorted(input_data.pictures, key=lambda x: x.number_of_tags, reverse=True)

        # Init score.
        strategy = BaseLineStrategy()
        solution = strategy.solve(input_data)
        scorer = Scorer2019Q(input_data)
        score = scorer.calculate(solution)

        # Change order of slides (flip), two at a time, if they have the same number of tags.
        # In total no more than n_flips.
        for position_picture_a, position_picture_b in zip(range(input_data.n_pictures - 1),
                                                          range(1, input_data.n_pictures)):

            # Stop if we have reached the maximum number of flips.
            if self.n_flips <= 0:
                break
            self.n_flips -= 1

            # Keep track of the score.
            print(self.n_flips, score)

            # Only flip if the two pictures have the same number of tags.
            if input_data.pictures[position_picture_a].number_of_tags != \
                    input_data.pictures[position_picture_b].number_of_tags:
                continue

            # Flip.
            input_data.pictures[position_picture_a], input_data.pictures[position_picture_b] = \
                input_data.pictures[position_picture_b], input_data.pictures[position_picture_a]

            # Recalculate score.
            candidate_solution = strategy.solve(input_data)
            candidate_score = scorer.calculate(candidate_solution)

            # If score improved, keep the solution.
            if candidate_score > score:
                solution = candidate_solution
                score = candidate_score
            else:
                # If score did not improve, flip back.
                input_data.pictures[position_picture_a], input_data.pictures[position_picture_b] = \
                    input_data.pictures[position_picture_b], input_data.pictures[position_picture_a]

                # Recalculate score.
                candidate_solution = strategy.solve(input_data)
                candidate_score = scorer.calculate(candidate_solution)
                assert candidate_score == score, "Flip is reversed, so score should not change."

        return solution
