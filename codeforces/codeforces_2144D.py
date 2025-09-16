import heapq
import math
import os
from collections import Counter, defaultdict, deque


def solve():
    """The new prices will be at least 1.
    x should be as small as possible in order to not reduce prices by too much, so x=2.
    However, if y is large, it can be better to use a larger x to reuse tickets
        i.e. subtract y fewer times.
    Too slow to check many values of x, because many values of c. 1 <= c <= 2e5
    Don't know how to quickly find value of x that reuses many labels.
    """
    n, y = list(map(int, input().split()))
    c = list(map(int, input().split()))


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
