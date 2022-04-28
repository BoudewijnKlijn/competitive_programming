from collections import Counter, defaultdict
from typing import List

from HC_2019_Qualification.slides import Slides


class NonZeroDefaultOrderStrategy:
    def order(self, score_values: List[int], score_rows: List[int], score_cols: List[int], solution: Slides,
              start_slide_id=None) -> Slides:
        """Add slides with non-zero transition.
        Start with the start slide id.
        :param score_values: list with integers, transition scores. NOT USED IN THIS STRATEGY
        :param score_rows: list with integers, that corresponds with index of slides in the solution.
        :param score_cols: list with integers, that corresponds with index of slides in the solution.
        :param solution: Slides, as created by another strategy.
        :param start_slide_id: int, slide id of old solution to start with. Use None to start with the slide that has
        the fewest number of non-zero transitions."""

        # Create dictionary: key=slide number. value=set with remaining slide ids with non-zero transition.
        remaining_slides_per_slide = defaultdict(set)
        for score_row, score_col in zip(score_rows, score_cols):
            remaining_slides_per_slide[score_row].add(score_col)

        # Track how many remaining slides with non-zero transition each slide has. Later, choose slide with the fewest options.
        # Key=slide id, value=number of remaining slides with non-zero transition.
        n_remaining_slides_per_slide = Counter(score_rows)

        # Track which slides have n non-zero transitions left over.
        c = Counter(score_rows)  # key=slide_id, value=number of non-zero transitions
        c2 = Counter(c.values())  # key=number of non-zero transitions, value=number of slides with that number of non-zero transitions
        slides_with_n_remaining_slides = {n: set() for n in range(max(c2.keys()) + 1)}
        for slide_id, n_transitions in n_remaining_slides_per_slide.items():
            slides_with_n_remaining_slides[n_transitions].add(slide_id)

        # Init
        slide_id = None
        slide_ids = list()
        slide_ids_set = set()
        n_zero_transitions = 0
        for i in range(len(c)):

            candidate_slide_ids = set()
            if slide_id is not None:
                # Get all remaining slides with non-zero transitions for last slide.
                candidate_slide_ids = remaining_slides_per_slide[slide_id]
                assert not any([candidate_slide_id in slide_ids_set for candidate_slide_id in candidate_slide_ids]), \
                    "Candidate slide id should not be already in slide_ids_set."

            # Find candidate with the minimum number of remaining options.
            candidate_is_found = False
            minimum_n_remaining_slides = None
            for candidate_slide_id in candidate_slide_ids:
                n_remaining_slides_candidate = n_remaining_slides_per_slide[candidate_slide_id]
                if minimum_n_remaining_slides is None or n_remaining_slides_candidate < minimum_n_remaining_slides:
                    minimum_n_remaining_slides = n_remaining_slides_candidate
                    best_candidate_slide_id = candidate_slide_id
                    candidate_is_found = True

                # Remove last slide from being an option for candidate slide. Regardless of whether it is the best candidate
                # or not. Also adjust the number of remaining slides for the candidate slide. Remove the candidate slide from
                # the set of slides with n remaining slides. Add the candidate slide to the set of slides with n-1 remaining
                remaining_slides_per_slide[candidate_slide_id].remove(slide_id)
                slides_with_n_remaining_slides[n_remaining_slides_per_slide[candidate_slide_id]].remove(
                    candidate_slide_id)
                n_remaining_slides_per_slide[candidate_slide_id] -= 1
                slides_with_n_remaining_slides[n_remaining_slides_per_slide[candidate_slide_id]].add(
                    candidate_slide_id)

            if candidate_is_found:
                new_slide_id = best_candidate_slide_id
                slides_with_n_remaining_slides[n_remaining_slides_per_slide[new_slide_id]].remove(new_slide_id)
            else:
                # Get new slide which has a zero transition score.
                n = 0  # Since we have zero transition with last slide, it could have zero remaining non-zero transitions.
                while not slides_with_n_remaining_slides[n]:
                    n += 1

                if start_slide_id is not None and i == 0:
                    # Only on the first run we can use the start slide.
                    new_slide_id = start_slide_id
                    slides_with_n_remaining_slides[n_remaining_slides_per_slide[new_slide_id]].remove(new_slide_id)
                else:
                    n_zero_transitions += 1
                    new_slide_id = slides_with_n_remaining_slides[n].pop()  # Just any slide. This is where start slide is chosen if not specified.

            # Add candidate as next slide
            slide_ids.append(new_slide_id)
            slide_ids_set.add(new_slide_id)

            # set up for new iteration
            slide_id = new_slide_id

        # solution = Slides([Slide(pictures=[input_data.pictures[candidate]]) for candidate in slide_ids])
        # scorer = Scorer2019Q(input_data)
        # score = scorer.calculate(solution)

        # score = max_score - n_zero_transitions * 3  # Alternative calculation that is much faster.
        # # assert score == score2, f"Score {score} != {score2}"
        #
        # return score

        return Slides([solution.slides[old_solution_slide_id] for old_solution_slide_id in slide_ids])
