import os
from collections import Counter


def solve():
    n, k = list(map(int, input().split()))

    s = list(map(int, input().split()))
    t = list(map(int, input().split()))

    # reduce to mod form
    s = Counter([min(si % k, abs(si % k - k)) for si in s])
    t = Counter([min(ti % k, abs(ti % k - k)) for ti in t])

    if s == t:
        print("YES")
    else:
        print("NO")


if __name__ == "__main__":
    MULTIPLE_TESTS = True

    if not os.path.exists("LOCAL"):
        t = 1
        if MULTIPLE_TESTS:
            t = int(input())

        for _ in range(t):
            solve()
    else:
        import test_runner

        test_runner.main(solve, __file__, MULTIPLE_TESTS)
