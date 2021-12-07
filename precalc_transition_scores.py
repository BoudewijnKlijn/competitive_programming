import operator
import os
import re
import time
from collections import Counter, defaultdict

import numpy as np
import pandas as pd
import scipy.sparse as ss
from sklearn.feature_extraction.text import CountVectorizer

from HC_2019_Qualification.Pictures import Pictures
from HC_2019_Qualification.scorer_2019_q import Scorer2019Q
from HC_2019_Qualification.slide import Slide
from HC_2019_Qualification.slides import Slides

start_time = time.time()

file_path = os.path.join('HC_2019_Qualification', 'input', 'b_lovely_landscapes.txt')
with open(file_path, 'r') as f:
    file_contents = f.read()

# Generator implementation (maybe better for larger inputs).
pattern = r'(t[a-z\d]*)'  # there are 2 occurrences of just the letter 't'
regex_group_iterator = re.finditer(pattern, file_contents)
tags = map(lambda x: x.group(1), regex_group_iterator)
unique_tags = list(set(tags))

# init
cv = CountVectorizer(vocabulary=unique_tags, token_pattern=pattern)

# transform data
lines = file_contents.strip().split('\n')[1:]  # skip the first input line
items = [line.split(' ') for line in lines]
ids = range(len(lines))
n_tags = [int(item[1]) for item in items]
tags = [' '.join(item[2:]) for item in items]

# make sparse matrix that contains all the tags of all the slides. has to be sparse because 80,000 x 839,999
matrix = cv.fit_transform(tags)

# check if matrix is as expected
assert matrix.min() == 0
assert matrix.max() == 1

# Calculate number of intersecting tags of one slide to another slide.
intersection_matrix = matrix @ matrix.transpose()

# Number of intersection with itself should be the number of tags.
assert intersection_matrix.diagonal().tolist() == list(n_tags)


# This gives COO format...
lower = ss.tril(intersection_matrix, 0)
upper = ss.triu(intersection_matrix, 0)

# transpose of either should be equal to the other. inequality is efficient apparently, whereas equality is not.
assert (lower.transpose() != upper).sum() == 0

# Sum should be the same as n_tags. This actually revealed that a tag my just be the letter 't' and nothing else.
sum_ = matrix.sum(axis=1)
assert all([operator.eq(a, b) for a, b in zip(sum_.flat, n_tags)])
for i, (idx, a, b) in enumerate(zip(ids, sum_.flat, n_tags)):
    if a != b:
        print(i, idx, a, b)

# Get the non zero elements and construct new sparse matrix with the number of tags on the non zero coordinates.
rows, cols = intersection_matrix.nonzero()
data = np.zeros_like(rows)  # init with zeros, and same shape as rows
for i, (r, c) in enumerate(zip(rows, cols)):
    data[i] = min(n_tags[r], n_tags[c])  # fill with minimum number of tags of the slides being compared
min_n_tags_matrix = ss.csr_matrix((data, (rows, cols)))

# Matrix with number of unique tags. The number of unique tags on the slide with fewer tags to be precise.
n_unique_tags_matrix = min_n_tags_matrix - intersection_matrix

# Matrix with the score (the lower value of number of tags or the intersection matrix).
score_matrix = n_unique_tags_matrix.minimum(intersection_matrix)

# Get the score values to calculate score statistics.
score_values = score_matrix.data
pd_scores = pd.Series(score_values)
# print(pd_scores.describe())  # statistics


score_rows, score_cols = score_matrix.nonzero()

# Construct slides for all transitions that have a score, and the score should match.
input_data = Pictures(file_path)

for score_row, score_col in zip(score_rows, score_cols):
    # print(score_row, score_col)
    slide_a = Slide(pictures=[input_data.pictures[score_row]])
    slide_b = Slide(pictures=[input_data.pictures[score_col]])

    assert Scorer2019Q.calculate_transition(slide_a, slide_b) == 3

c = Counter(score_rows)  # key=slide_id, value=number of non-zero transitions
c2 = Counter(c.values())  # key=number of non-zero transitions, value=number of slides with that number of non-zero transitions

assert sum(c2.values()) == 80000


# Create dictionary: key=slide number. value=set with remaining slide ids with non-zero transition.
remaining_slides_per_slide = defaultdict(set)
for score_row, score_col in zip(score_rows, score_cols):
    remaining_slides_per_slide[score_row].add(score_col)

# Track how many remaining slides with non-zero transition each slide has. Later, choose slide with the  fewest options.
# Key=slide id, value=number of remaining slides with non-zero transition.
n_remaining_slides_per_slide = Counter(score_rows)

# Track which slides have n non-zero transitions left over.
slides_with_n_remaining_slides = {n: set() for n in range(max(c2.keys()) + 1)}
for slide_id, n_transitions in n_remaining_slides_per_slide.items():
    slides_with_n_remaining_slides[n_transitions].add(slide_id)


# Init
slide_id = None
slide_ids = list()
slide_ids_set = set()
for _ in range(80_000):

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
        slides_with_n_remaining_slides[n_remaining_slides_per_slide[candidate_slide_id]].remove(candidate_slide_id)
        n_remaining_slides_per_slide[candidate_slide_id] -= 1
        slides_with_n_remaining_slides[n_remaining_slides_per_slide[candidate_slide_id]].add(candidate_slide_id)

    if candidate_is_found:
        new_slide_id = best_candidate_slide_id
        slides_with_n_remaining_slides[n_remaining_slides_per_slide[new_slide_id]].remove(new_slide_id)
    else:
        # Get new slide which has a zero transition score.
        n = 0  # Since we have zero transition with last slide, it could have zero remaining non-zero transitions.
        while not slides_with_n_remaining_slides[n]:
            n += 1
        new_slide_id = slides_with_n_remaining_slides[n].pop()  # Just any slide.

    # Add candidate as next slide
    slide_ids.append(new_slide_id)
    slide_ids_set.add(new_slide_id)

    # set up for new iteration
    slide_id = new_slide_id

solution = Slides([Slide(pictures=[input_data.pictures[candidate]]) for candidate in slide_ids])
scorer = Scorer2019Q(input_data)
score = scorer.calculate(solution)

max_score = (80000-1) * 3

print(f'Score: {score} ({score / max_score * 100:.3f}% of maximum score which is {max_score})')

print(f'Time: {time.time() - start_time:.2f} seconds')
