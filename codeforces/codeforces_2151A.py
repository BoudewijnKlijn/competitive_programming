import bisect
import heapq
import math
import os
from collections import Counter, defaultdict, deque


def solve():
    n, m = list(map(int, input().split()))
    a = list(map(int, input().split()))

    # test whether a is increasing
    is_increasing = True
    prev = None
    for aa in a:
        if prev is None or aa > prev:
            prev = aa
            continue
        is_increasing = False
        break

    if is_increasing:
        maxi = a[-1]
        print(n - maxi + 1)
    else:
        print(1)


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
