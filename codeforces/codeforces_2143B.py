import heapq
import math
import os
from collections import Counter, defaultdict, deque


def solve():
    """It's always better to use a discount if possible.
    It's also always better to apply discount to most expensive items first.
    Sort prices.
    Sort discount.
    Apply discounts for fewer items on most expensive items, such that most expensive items are free.
    """
    n, k = list(map(int, input().split()))
    a = sorted(map(int, input().split()), reverse=True)  # high to low
    b = sorted(map(int, input().split()))  # low to high

    ans = 0
    idxa = 0
    for bb in b:
        if idxa + bb - 1 < n:
            # cheapest one is free
            ans += sum(a[idxa : idxa + bb - 1])
            idxa += bb
        else:
            # pay for all
            ans += sum(a[idxa:])
            idxa += bb
            break
    ans += sum(a[idxa:])
    print(ans)


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
