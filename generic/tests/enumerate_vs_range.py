"""`for i in range(n)` is fastest.
`enumerate` is ~10% slower.
one-liner is ~50% slower."""

import os
import random
import sys
from math import prod

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from generic.timer import compare

N = 1_000
nums = [random.randint(0, N) for _ in range(N)]
nums2 = [random.randint(0, N) for _ in range(N)]


def i_in_range():
    n = len(nums)
    sum_prod = 0
    for i in range(n):
        sum_prod += i * nums[i]
    return sum_prod


def enumerate_():
    sum_prod = 0
    for i, num in enumerate(nums):
        sum_prod += i * num
    return sum_prod


def one_liner():
    return sum(map(prod, enumerate(nums)))


def one_liner_lambda():
    return sum(map(lambda x: x[0] * x[1], enumerate(nums)))


if __name__ == "__main__":
    compare(
        [i_in_range, enumerate_, one_liner, one_liner_lambda],
        os.path.abspath(__file__),
        number=100,
        repeat=1_000,
    )
    # Raw medians:
    # i_in_range          0.004919
    # enumerate_          0.005565
    # one_liner           0.007273
    # one_liner_lambda    0.008257
    # dtype: float64

    # Scaled medians (relative to best):
    # i_in_range          0.990798
    # enumerate_          1.128705
    # one_liner           1.470544
    # one_liner_lambda    1.676276
    # dtype: float64
