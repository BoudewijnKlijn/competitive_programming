import os


def solve():
    n, m, a = map(int, input().split())
    horizontal = n // a if n % a == 0 else n // a + 1
    vertical = m // a if m % a == 0 else m // a + 1
    print(horizontal * vertical)


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
