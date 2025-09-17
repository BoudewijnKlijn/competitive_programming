import bisect
import heapq
import math
import os
from collections import Counter, defaultdict, deque


def solve():
    """A subsequence which contains a,b,c where a>b>c is not good.
        Because a and b must have different colors and a and c as well as b and c too.
        This is not possible.
        If this subsequence is not present, it must be good.
    All sequences of length 0, 1, and 2 are thus good.
    Just as in problem statement, maybe easier to compute total number of possibilities and
        then subtract invalid combinations.
    If a new number is equal or higher than current maximum, it is always good to combine with all
        existing subsequences.
    So, I could use binary search to check that is is larger than x values before it.
    ...This is not correct, because I know that values are smaller than numbers before, but not
        the order of numbers before. It may be smaller than all of them but if they were increasing
        all the time, its still a good array.
    """
    n = int(input())
    a = list(map(int, input().split()))
    values = []
    for idx in range(n):
        val = a[idx]
        insert_idx = bisect.bisect(values, val)
        values.insert(insert_idx, val)
        print(values)

    total = 2**n


if __name__ == "__main__":
    MULTIPLE_TESTS = True

    if not os.path.exists(os.path.join("codeforces", "LOCAL")):
        t = 1
        if MULTIPLE_TESTS:
            t = int(input())

        for _ in range(t):
            solve()
    else:
        import test_runner

        test_runner.main(solve, __file__, MULTIPLE_TESTS)
