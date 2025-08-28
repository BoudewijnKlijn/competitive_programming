import os
from collections import deque


def solve():
    """Yes it is possible if the maximum number of consecutive 1's is less than k.
    A valid permutation can be constructed from giving the zeros the highest number and divide
    the remaining over the 1's."""
    n, k = list(map(int, input().split()))
    s = list(map(int, input()))
    streak = 0
    ans = list()
    permutation = deque(range(n, 0, -1))
    for si in s:
        if si:
            streak += 1
            ans.append(permutation.pop())
        else:
            streak = 0
            ans.append(permutation.popleft())
        if streak >= k:
            print("NO")
            return
    print("YES")
    print(*ans)


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
