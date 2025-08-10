import os


def solve():
    _ = int(input())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    ans = 0
    ignored = False
    while not ignored:
        # step 1: find i for which a > b
        for i, (ai, bi) in enumerate(zip(a, b)):
            if ai > bi:
                a[i] -= 1
                break
        else:
            ignored = True

        # step 2: find i for which a < b
        for i, (ai, bi) in enumerate(zip(a, b)):
            if ai < bi:
                a[i] += 1
                break
        ans += 1

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
