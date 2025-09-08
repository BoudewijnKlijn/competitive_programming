import os


def solve():
    """The best oven to collect from depends on how quickly new cakes appear and
        if collected before.
    If n < m, it only matters what we do in the last n seconds, because cookies
        will accumulate in ovens.
    With the same reasoning, it makes sense to end with the best oven, and start
    with the slowest accumulating oven (?)
    """
    _, m = list(map(int, input().split()))
    a = list(map(int, input().split()))
    a.sort(reverse=True)  # highest to lowest
    ans = 0
    for aa in a:
        if m == 0:
            break
        ans += aa * m
        m -= 1
    print(ans)


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
