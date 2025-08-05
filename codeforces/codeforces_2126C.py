import os


def solve():
    """Teleporting with the smallest step possible is guaranteed to be best.
    If height is equal, teleporting takes no time, so not necessary to remove duplicate heights.
    Sort heights, and then move right, to alwayws move up with smallest step.
    """
    n, k = map(int, input().split())
    heights = list(map(int, map(int, input().split())))
    current_height = heights[k - 1]
    heights.sort()
    goal_height = heights[-1]

    # find starting point
    i = 0
    while heights[i] < current_height:
        i += 1

    time = 0
    while heights[i] < goal_height:
        time_to_complete = heights[i + 1] - heights[i]
        if time + time_to_complete > heights[i]:
            print("NO")
            return

        i += 1
        time += time_to_complete
    print("YES")


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
