import os


def solve():
    a, b, c, d = list(map(int, input().split()))

    def solve_half(goal1, goal2):
        goal_min, goal_max = min(goal1, goal2), max(goal1, goal2)
        if goal_max > 2 + 2 * goal_min:
            return False
        else:
            return True

    if not solve_half(a, b) or not solve_half(c - a, d - b):
        print("NO")
    else:
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
