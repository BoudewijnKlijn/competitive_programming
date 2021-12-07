import operator
import os
import re
from collections import Counter, defaultdict

import numpy as np
import pandas as pd
import scipy.sparse as ss
from sklearn.feature_extraction.text import CountVectorizer

from HC_2019_Qualification.Pictures import Pictures
from HC_2019_Qualification.scorer_2019_q import Scorer2019Q
from HC_2019_Qualification.slide import Slide
from HC_2019_Qualification.slides import Slides

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
print(pd_scores.describe())  # statistics


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

# Note: I did not use upper or lower triangle so the score rows and cols contains double pairs.
# e.g. for the first slide
slide_id = 0
slides_with_non_zero = score_cols[score_rows == slide_id]
for slide_b in slides_with_non_zero:
    slides_with_non_zero_slide_b = score_rows[score_cols == slide_b]
    print(slide_id, slide_b, slides_with_non_zero_slide_b)


# Start making transitions with slides that have the minimum number of non-zero transitions.
slides_with_2_transitions = [slide_id for slide_id, n_transitions in c.items() if n_transitions == 2]

# Create dictionary with non-zero transitions. Key is slide number. Value is list of slide ids with non-zero transitions
slides_with_non_zero_transitions = defaultdict(set)
for score_row, score_col in zip(score_rows, score_cols):
    slides_with_non_zero_transitions[score_row].add(score_col)  # TODO: could be set as well, but I like to maintain order

# Sort dictionary on number of non-zero transitions.
slides_with_non_zero_transitions = dict(sorted(slides_with_non_zero_transitions.items(), key=lambda x: len(x[1])))


# Init
start_slide_id = slides_with_2_transitions[0]
slides_ids = [start_slide_id]
slide_set = {start_slide_id}


i = 1
while i < 80000:
    i += 1
    # if i > 10000:
    #     break
    if i % 1000 == 0:
        print(i, len(slide_set))

    # Get next slide id. Loop over all connection with last slide
    last_slide_id = slides_ids[-1]
    candidate_slide_ids = slides_with_non_zero_transitions[last_slide_id] - slide_set
    new_slide_added = False
    for candidate_id in candidate_slide_ids:
        slide_set.add(candidate_id)
        slides_ids.append(candidate_id)
        new_slide_added = True
        break

    if not new_slide_added:
        # No slide added, so all candidates had been added before. Choose new start slide.
        candidate_slide_ids = set(slides_with_non_zero_transitions.keys()) - slide_set  # todo: check if this maintained order of keys
        for candidate_id in candidate_slide_ids:
            slide_set.add(candidate_id)
            slides_ids.append(candidate_id)
            break

    # Code is slow to finish. Just dump the remaining 40k slides at the end and see what the score is.
    # TODO: improve, e.g. by keeping track of how many options are left for a slide. Shuffle the slides to create randomness at start
    if i > 40_000:
        unused_slides = set(slides_with_non_zero_transitions.keys()) - slide_set
        slides_ids.extend(unused_slides)
        break

solution = Slides([Slide(pictures=[input_data.pictures[candidate]]) for candidate in slides_ids])
scorer = Scorer2019Q(input_data)
score = scorer.calculate(solution)

print(f'Score: {score}')