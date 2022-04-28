from random import Random

from HC_2019_Qualification.Pictures import Pictures
from HC_2019_Qualification.slides import Slides
from HC_2019_Qualification.strategies.baseline_solver import BaseLineStrategy
from valcon.strategies.strategy import Strategy
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
        n_slides = len(solution.slides)
        for position_slide_a, position_slide_b in zip(range(n_slides - 1), range(1, n_slides)):

            # Stop if we have reached the maximum number of flips.
            if self.n_flips <= 0:
                break
            self.n_flips -= 1

            # Keep track of the score.
            print(self.n_flips, score)

            # Only flip if the two pictures have the same number of tags.
            if solution.slides[position_slide_a].number_of_tags != \
                    solution.slides[position_slide_b].number_of_tags:
                continue

            # Determine impact on score due to the flip. If we flip adjacent slides, only the scores of two transitions
            # are affected (only the score of the transition of the first slide and the slide before that, and the score
            # of the transition of the last slide and the slide after that are affected). Instead of recalculating
            # n_picture - 1 transitions, we can just recalculate the transition of the first slide and the transition of
            # the last slide and add the difference to the score.
            transition_a_score_delta = 0
            if position_slide_a > 0:
                before = scorer.calculate_transition(
                    solution.slides[position_slide_a - 1],
                    solution.slides[position_slide_a]
                )
                after = scorer.calculate_transition(
                    solution.slides[position_slide_a - 1],
                    solution.slides[position_slide_b]
                )
                transition_a_score_delta = after - before
            transition_b_score_delta = 0
            if (position_slide_b + 1) < n_slides:
                before = scorer.calculate_transition(
                    solution.slides[position_slide_b],
                    solution.slides[position_slide_b + 1]
                )
                after = scorer.calculate_transition(
                    solution.slides[position_slide_a],
                    solution.slides[position_slide_b + 1]
                )
                transition_b_score_delta = after - before
            score_delta = transition_a_score_delta + transition_b_score_delta

            # Update the solution and score, if the score_delta is non-negative.
            if score_delta >= 0:
                solution.slides[position_slide_a], solution.slides[position_slide_b] = \
                    solution.slides[position_slide_b], solution.slides[position_slide_a]

            assert score == scorer.calculate(solution), \
                "Score calculated via deltas should match with complete calculation."

        return solution
