"""Codeforces is 10 letters/positions.
It can be viewed as 1x1x1x1x1x1x1x1x1x1 = 1 ** 10 = 1
Adding an s to the end gives 1 ** 9 * 2 = 2
We can add another s to the end which gives 1 ** 9 * 3 = 3
Or we can duplicate another letter which gives 1 ** 8 * 2 * 2 = 4, which is better
Thereafter it is best to increase another 1 to a 2 instead of a 2 to a 3.
1 ** 8 * 2 * 3 = 6 < 1 ** 7 * 2 * 2 * 2 = 8
so CODEFORCEESSS < CODEFORCCEESS

1 ** 6 * 2 * 2 * 2 * 2 = 16 and 1 ** 7 * 2 * 2 * 3 = 12
"""
from math import prod
from typing import List


def calc_score(array: List[int]) -> int:
    return prod(array)


goal = int(input())
string = 'codeforces'

counts = [1] * 10

while calc_score(counts) < goal:
    best_score = 0
    for pos in range(10):
        counts_copy = counts.copy()
        counts_copy[pos] += 1
        trial = prod(counts_copy)
        if trial > best_score:
            best_score = trial
            best_copy = counts_copy
    counts = best_copy

ans = ''.join([s * x for s, x in zip(string, counts)])
print(ans)





