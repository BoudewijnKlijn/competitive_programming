import os

def solve():
    a = int(input())
    numbers = list(map(int, input().split()))
    assert len(numbers) == a

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
