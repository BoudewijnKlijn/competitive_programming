from collections import Counter

import operator
from valcon import InputData
from valcon.scorer import Scorer
from HC_2019_Qualification.slides import Slides
import itertools
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import scipy.sparse as ss
import pandas as pd
from typing import List, Tuple, Dict, Set, Optional


class Scorer2019Q(Scorer):
    """
    Validate input (slide with only 1 V should raise error)
    """

    @staticmethod
    def calculate_transition(slide_a, slide_b):
        intersection_size = len(slide_a.tags & slide_b.tags)
        set_minus_size = slide_a.number_of_tags - intersection_size
        set_minus_size_2 = slide_b.number_of_tags - intersection_size
        return min(intersection_size, set_minus_size, set_minus_size_2)

    def calculate(self, slides: Slides) -> int:
        score = 0
        for slide_a, slide_b in zip(slides.slides[:-1], slides.slides[1:]):
            score += self.calculate_transition(slide_a, slide_b)
        return score

    def __init__(self, input_data: InputData):
        pass


def get_non_zero_slide_transitions(slides: Slides, validate=True) -> Tuple[List[int], List[int], List[int]]:
    """This function is not suitable for problem D and E (it seems). Those have few tags, maybe use normal matrices."""

    if validate:
        print('Start calculation of non-zero scores...')
    pattern = r'([a-z\d]+)'
    tags_of_slides = [' '.join(slide.tags) for slide in slides.slides]
    number_of_tags_of_slides = [slide.number_of_tags for slide in slides.slides]
    n_tags_all_slides = sum(number_of_tags_of_slides)
    unique_tags = list(set(itertools.chain.from_iterable(map(str.split, tags_of_slides))))
    density = n_tags_all_slides / (len(tags_of_slides) * len(unique_tags))
    sparse = True if density < 1 / 1000 else False

    if validate:
        print(f'Number of slides: {len(tags_of_slides)}\n'
              f'Sum of number of tags on all slides {n_tags_all_slides}\n'
              f'Most tags on one slide: {max(number_of_tags_of_slides)}\n'
              f'Number of unique tags {len(unique_tags)}\n'
              f'Density: {density}')

    cv = CountVectorizer(vocabulary=unique_tags, token_pattern=pattern)

    matrix = cv.fit_transform(tags_of_slides)

    if validate:
        print(f'Number of slides: {len(tags_of_slides)}\n'
              f'Number of unique tags {len(unique_tags)}')
        # check if matrix is as expected
        assert matrix.min() == 0
        assert matrix.max() == 1

    # Calculate number of intersecting tags of one slide to another slide.
    intersection_matrix = matrix @ matrix.transpose()

    if validate:
        # Number of intersection with itself should be the number of tags.
        assert intersection_matrix.diagonal().tolist() == number_of_tags_of_slides

        # This gives COO format...
        lower = ss.tril(intersection_matrix, 0)
        upper = ss.triu(intersection_matrix, 0)
        # transpose of either should be equal to the other. inequality is efficient apparently, whereas equality is not.
        assert (lower.transpose() != upper).sum() == 0

        # Sum should be the same as n_tags. This actually revealed that a tag may just be the letter 't' and nothing else.
        sum_ = matrix.sum(axis=1)
        assert all([a == b for a, b in zip(sum_.flat, number_of_tags_of_slides)])

    # Get the non zero elements and construct new sparse matrix with the number of tags on the non zero coordinates.
    rows, cols = intersection_matrix.nonzero()
    data = np.zeros_like(rows)  # init with zeros, and same shape as rows
    for i, (r, c) in enumerate(zip(rows, cols)):
        data[i] = min(number_of_tags_of_slides[r], number_of_tags_of_slides[c])  # fill with minimum number of tags of the slides being compared
    min_n_tags_matrix = ss.csr_matrix((data, (rows, cols)))

    # Matrix with number of unique tags. The number of unique tags on the slide with fewer tags to be precise.
    n_unique_tags_matrix = min_n_tags_matrix - intersection_matrix

    # Matrix with the score (the lower value of number of tags or the intersection matrix).
    score_matrix = n_unique_tags_matrix.minimum(intersection_matrix)

    # Get the score values to calculate score statistics.
    score_values = score_matrix.data
    # pd_scores = pd.Series(score_values)
    # print(pd_scores.describe())  # statistics

    score_rows, score_cols = score_matrix.nonzero()
    if validate:
        assert len(score_values) == len(score_rows) == len(score_cols)

        # Construct slides for all transitions that have a score, and the score should match.
        scorer = Scorer2019Q(None)
        for score_value, score_row, score_col in zip(score_values, score_rows, score_cols):
            # print(score_row, score_col)
            slide_a = slides.slides[score_row]
            slide_b = slides.slides[score_col]

            assert scorer.calculate_transition(slide_a, slide_b) == score_value

        c = Counter(score_rows)  # key=slide_id, value=number of non-zero transitions
        c2 = Counter(c.values())  # key=number of non-zero transitions, value=number of slides with that number of non-zero transitions

        assert sum(c2.values()) == len(slides.slides)

        print('Non-zero scores calculated.')

    return score_values, score_rows, score_cols
