import operator
import os
import re

import numpy as np
import pandas as pd
import scipy.sparse as ss
from sklearn.feature_extraction.text import CountVectorizer

from HC_2019_Qualification.Pictures import Pictures
from HC_2019_Qualification.slide import Slide
from HC_2019_Qualification.scorer_2019_q import Scorer2019Q

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
