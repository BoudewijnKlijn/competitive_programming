import os


def solve():
    """When is GCD < 3, only when GCD = 1 or 2.
    GCD 1 means no common divisors, e.g. two primes.
    GCD 2 means greatest divisor is 2, e.g. powers of two.
    If all numbers are divisable by 3, then 3 is GCD, which is definitely valid.
    Other option is make everything equal to n+1. Since n >= 2, the greatest common divisor
        will be n+1, which is always >= 3.
    """
    n = int(input())
    p = list(map(int, input().split()))
    q = [n + 1 - pp for pp in p]
    print(*q)


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
