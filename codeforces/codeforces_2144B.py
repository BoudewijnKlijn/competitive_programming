import heapq
import os
from collections import Counter, defaultdict, deque


def solve():
    """We know that the entire array has to be sorted AND contain the numbers from 1 to n.
    From the start and from the end, check how many numbers are already in correct spot.
    If just one zero in entire array, can only be replaced by one integer.
    Find missing value and replace the zero.
    Numbers in correct place are subtracted from the maximum cost: n.
    """
    n = int(input())
    a = list(map(int, input().split()))

    n_zeros = a.count(0)
    if n_zeros == 1:
        missing = set(range(1, n + 1)) - set(a) - {0}
        a[a.index(0)] = missing.pop()

    n_skipped = 0
    for i, aa in enumerate(a, start=1):
        if i != aa:
            break
        n_skipped += 1

    if n_skipped == n:
        # stop here. everything is already sorted
        print(0)
        return

    n_skipped_from_end = 0
    for i, aa in enumerate(reversed(a)):
        if n - i != aa:
            break
        n_skipped_from_end += 1

    ans = n - n_skipped - n_skipped_from_end
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
