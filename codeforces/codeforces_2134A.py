import os


def solve():
    """If n is odd, and b >= a, and b odd as well, its definitely possible. Paint over the red.
    If n is even, and b is odd, not possible."""
    n, a, b = list(map(int, input().split()))
    if n % 2:  # n is odd
        if b >= a:  # doesnt matter what a is.
            if b % 2:
                print("YES")
            else:
                print("NO")
        else:
            if b % 2 and a % 2:
                print("YES")
            else:
                print("NO")
    else:
        if b >= a:  # doesnt matter what a is.
            if b % 2:
                print("NO")
            else:
                print("YES")
        else:
            if (b % 2 == 0) and (a % 2 == 0):
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
