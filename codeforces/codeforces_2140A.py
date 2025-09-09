import heapq
import os
import sys
from collections import Counter, defaultdict, deque


def solve():
    """The left or right shift with 3 values is almost identical to swapping.
    Can use left and right pointer to swap values."""
    input = sys.stdin.readline
    n = int(input().strip())
    s = input().strip()
    left, right = 0, n - 1
    ans = 0
    for left, char in enumerate(s):
        if char == "0":
            continue

        while right >= left and s[right] == "1":
            right -= 1

        if left >= right:
            break

        ans += 1
        right -= 1

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
