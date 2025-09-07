import os


def solve():
    """Can always just multiply with 2 k times.
    But, k could be huge. No limit, just larger than 1.
        So its safer to try all x, and see what the loop is. Then mod loop, so even for huge k valid.
    x could be negative... but lets assume it doesnt.
    """
    # k, x = list(map(int, input().split()))
    # while k > 0:
    #     x *= 2
    #     k -= 1
    # print(x)

    # # # todo find solution for very large k. to be hackable proof.
    # k, x = list(map(int, input().split()))
    # mapping = dict()
    # for start in range(21):
    #     seen = list()


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
