import os


def get_coins(x):
    return int(3 ** (x + 1) + x * 3 ** (x - 1))


def solve():
    n = int(input())
    x = 100
    ans = 0
    while n > 0:
        while 3**x > n:
            x -= 1
        n -= 3**x
        ans += get_coins(x)
    print(ans)


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
