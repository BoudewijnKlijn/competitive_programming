# numbers = tuple(map(int, open('in2', 'r').read().split()))
# numbers = tuple(map(int, open('in3', 'r').read().split()))
# numbers = tuple(map(int, open('in4', 'r').read().split()))
import os
from collections import Counter

def solve():
    _ = int(input())
    numbers = tuple(map(int, input().split()))
    c = Counter(numbers)
    numbers = sorted(set(numbers))
    scores = dict()
    for n in range(max(numbers)+1):
        for chosen in [0, 1]:
            if chosen:
                scores[(n, chosen)] = c.get(n, 0) * n + max(scores.get((n-2, 0), 0), scores.get((n-2, 1), 0))
            else:
                scores[(n, chosen)] = max(scores.get((n-1, 0), 0), scores.get((n-1, 1), 0))
    print(max(list(scores.values())))

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
