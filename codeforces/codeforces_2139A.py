import os


def solve():
    a, b = list(map(int, input().split()))
    a, b = min(a, b), max(a, b)  # make b the larger number

    if a == b:
        print(0)
    elif b % a == 0:
        print(1)
    else:
        print(2)


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
