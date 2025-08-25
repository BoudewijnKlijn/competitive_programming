"""Using first element is fastest.
Initializing with None takes ~10% longer.
Using zip takes ~30% longer."""

import os
import random
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from generic.timer import compare

N = 1_000
nums = [random.randint(0, N) for _ in range(N)]


def prev_none():
    prev = None
    for num in nums:
        if prev is None:
            prev = num
            continue

        # do something with prev and num
        ans = prev + num

        prev = num


def prev_first():
    prev = nums[0]
    for num in nums[1:]:
        # do something with prev and num
        ans = prev + num

        prev = num


def zip_():
    for prev, num in zip(nums, nums[1:]):
        # do something with prev and num
        ans = prev + num


if __name__ == "__main__":
    compare(
        [prev_none, prev_first, zip_],
        os.path.abspath(__file__),
        number=100,
        repeat=1_000,
    )
    # Raw medians:
    # prev_none     0.003296
    # prev_first    0.002934
    # zip_          0.003791
    # dtype: float64

    # Scaled medians (relative to best):
    # prev_none     1.120424
    # prev_first    0.992094
    # zip_          1.287792
    # dtype: float64
