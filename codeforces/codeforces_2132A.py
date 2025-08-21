import os


def solve():
    _ = int(input())
    a = input()
    _ = int(input())
    b = input()
    c = input()

    for bb, cc in zip(b, c):
        if cc == "V":
            a = bb + a
        else:
            a += bb
    print(a)


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
