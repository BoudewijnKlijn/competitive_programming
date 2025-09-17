import heapq
import math
import os
from collections import Counter, defaultdict, deque


def solve():
    """It is possible if we can constantly expand the area by 1.
    Sort of like an oil spill.
    """
    n = int(input())
    p = list(map(int, input().split()))
    idx_max = p.index(n)
    left, right = idx_max, idx_max
    val = n
    while val > 1:
        if left - 1 >= 0 and p[left - 1] == val - 1:
            left -= 1
        elif right + 1 < n and p[right + 1] == val - 1:
            right += 1
        else:
            print("NO")
            return
        val -= 1
    print("YES")


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
