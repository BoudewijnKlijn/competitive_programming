import os
import re
import operator

import numpy as np
import scipy.sparse as ss
from sklearn.feature_extraction.text import CountVectorizer

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
combinations = sorted(zip(ids, n_tags, tags), key=lambda x: x[1])

ids_sorted, n_tags_sorted, tags_sorted_by_n_tags = zip(*combinations)

matrix = cv.fit_transform(tags_sorted_by_n_tags)

# check if matrix is as expected
assert matrix.min() == 0
assert matrix.max() == 1

# Calculate number of intersecting tags of one slide to another slide.
intersection_matrix = matrix @ matrix.transpose()

# Number of intersection with itself should be the number of tags.
assert intersection_matrix.diagonal().tolist() == list(n_tags_sorted)


# This gives COO format...
lower = ss.tril(intersection_matrix, 0)
upper = ss.triu(intersection_matrix, 0)

# transpose of either should be equal to the other. inequality is efficient apparently, whereas equality is not.
assert (lower.transpose() != upper).sum() == 0

# Sum should be the same as n_tags. This actually revealed that a tag my just be the letter 't' and nothing else.
sum_ = matrix.sum(axis=1)
assert all([operator.eq(a, b) for a, b in zip(sum_.flat, n_tags_sorted)])
for i, (idx, a, b) in enumerate(zip(ids_sorted, sum_.flat, n_tags_sorted)):
    if a != b:
        print(i, idx, a, b)

# Get the non zero elements and construct new sparse matrix with the number of tags on the non zero coordinates.
rows, cols = intersection_matrix.nonzero()
data = np.zeros_like(rows)  # init with zeros, and same shape as rows
for i, (r, c) in enumerate(zip(rows, cols)):
    data[i] = min(n_tags_sorted[r], n_tags_sorted[c])  # fill with minimum number of tags of the slides being compared
min_n_tags_matrix = ss.csr_matrix((data, (rows, cols)))

# Matrix with number of unique tags. The number of unique tags on the slide with fewer tags to be precise.
delta_matrix = min_n_tags_matrix - intersection_matrix

# Matrix with the score (the lower value of number of tags or the intersection matrix).
score_matrix = delta_matrix.minimum(intersection_matrix)