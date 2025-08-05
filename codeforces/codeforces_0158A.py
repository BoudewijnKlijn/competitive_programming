import os
from math import prod


def solve():
    # n = int(input())
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    cutoff = a[k]
    ans = 0
    for score in a:
        if score >= cutoff and score > 0:
            ans += 1
        else:
            break

    print(ans)


if __name__ == "__main__":
    MULTIPLE_TESTS = False
    if not os.path.exists("LOCAL"):

        t = 1
        if MULTIPLE_TESTS:
            t = int(input())

        for _ in range(t):
            solve()
    else:
        import test_runner

        test_runner.main(solve, __file__, MULTIPLE_TESTS)
