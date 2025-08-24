import os


def solve():
    """Output YES if a single gear occurs twice."""
    _ = int(input())
    a = list(map(int, input().split()))
    seen = set()
    for gear in a:
        if gear in seen:
            print("YES")
            return
        seen.add(gear)
    print("NO")


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
