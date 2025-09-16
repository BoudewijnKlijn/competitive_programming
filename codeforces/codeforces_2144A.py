import heapq
import os
from collections import Counter, defaultdict, deque


def solve():
    """n is small (40), so O(n**2) solution will suffice."""
    n = int(input())
    a = list(map(int, input().split()))

    for left in range(n):
        left_sum = sum(a[: left + 1])
        for right in range(left + 1, n):
            mid_sum = sum(a[left + 1 : right + 1])
            right_sum = sum(a[right + 1 :])

            left_sum_mod_3 = left_sum % 3
            mid_sum_mod_3 = mid_sum % 3
            right_sum_mod_3 = right_sum % 3
            if (
                left_sum_mod_3 == mid_sum_mod_3 and left_sum_mod_3 == right_sum_mod_3
            ) or (
                left_sum_mod_3 != mid_sum_mod_3
                and left_sum_mod_3 != right_sum_mod_3
                and mid_sum_mod_3 != right_sum_mod_3
            ):
                print(left + 1, right + 1)
                return
    print(0, 0)


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
