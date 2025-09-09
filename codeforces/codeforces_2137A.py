import os


def solve():
    """Can always just multiply with 2 k times.
    1 <= k, x <= 20
    """
    k, x = list(map(int, input().split()))
    while k > 0:
        x *= 2
        k -= 1
    print(x)


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
