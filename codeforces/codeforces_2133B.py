import heapq
import os


def solve():
    """Steve has to give emeralds equal to max(a,b) and their values decreases by min(a,b).
    So, it makes sense to combine two higher value together. Otherwise he has to give many
    emeralds another time. And values decrease by less as well.
    Only necessary to link people, not combine everyone with everyone."""
    _ = int(input())
    g = list(map(lambda x: -int(x), input().split()))
    heapq.heapify(g)
    # match two highest. remove the largest thereafter.
    # the smallest becomes zero or is zero already. adding it to queue won't matter
    # terminate when two zeros are matched since that wont increase score.
    ans = 0
    while len(g) > 1:
        a = -1 * heapq.heappop(g)
        b = -1 * heapq.heappop(g)
        if not a and not b:
            print(ans)
            return
        ans += max(a, b)
        heapq.heappush(g, 0)
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
