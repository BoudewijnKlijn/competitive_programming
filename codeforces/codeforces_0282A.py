import os


def solve():
    n = int(input())
    ans = 0
    for _ in range(n):
        for char in input():
            if char == "X":
                continue
            elif char == "-":
                ans -= 1
            else:
                ans += 1
            break
    print(ans)


if __name__ == "__main__":
    MULTIPLE_TESTS = False

    if not os.path.exists("LOCAL"):
        t = 1
        if MULTIPLE_TESTS:
            t = int(input())

        for _ in range(t):
            solve()
    else:
        import test_runner

        test_runner.main(solve, __file__, MULTIPLE_TESTS)
