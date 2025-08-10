import os


def solve():
    n = int(input())

    ans = [-1, 3] * ((n + 1) // 2)
    ans = ans[:n]
    if ans[-1] == 3:
        ans[-1] = 2
    print(" ".join(map(str, ans)))


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
