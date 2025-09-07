import os


def solve():
    """The largest sum must be obtained when either a or b is at its largest value,
    provided that sum is even. Otherwise divide with smallest number to make it even.
    Dividing by an odd k, doesnt change the sums odd/evenness (if odd before, still odd.
    if even before, still even).
    Dividing (and multiplying) with even k, does make a even (if it wasnt) and b remains even
        if it still has another even factor.
        Dividing by 2 is always best and always possible when even.
    Then to get largest number, a or b should be as small as possible.
    a or b could be a huge prime. so checking for primes up to 10*18 is not feasible.
    But if just now b has 2 as prime factor, then we know a gets multiplied by b/2.
    """
    a, b = list(map(int, input().split()))

    # its possible if both a and b have an even factor (both are even)
    # or if both are odd
    if a % 2 == 0 and b % 2 == 0:
        print(a * b // 2 + 2)
    # a odd initially, but can make a even, and b still even as well.
    elif b % 4 == 0:
        print(a * b // 2 + 2)
    # both odd. reduce b to 1, so all divide by all factors
    elif a % 2 == 1 and b % 2 == 1:
        print(a * b + 1)
    else:
        print(-1)


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
