import os
from math import prod


def solve():
    # n = int(input())
    arr = list(map(int, input().split()))
    print(prod(arr) // 2)


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
