import heapq
import os
from collections import Counter, defaultdict, deque


def solve():
    """It's possible if b value occurs a multiple of b times."""
    n = int(input())
    b = list(map(int, input().split()))

    # two purposes:
    # - get indices of each value
    # - use len to get number of values
    pos = defaultdict(list)
    for i in range(n):
        pos[b[i]].append(i)

    # b must occur a multiple of b times. otherwise not possible
    # insert correct values
    #   some b_value may occur more often than value itself, e.g. b=1.
    #   then have to insert several values
    ans = [0] * n
    replace_val = 1
    for b_value, idxs in pos.items():
        if len(idxs) < b_value or len(idxs) % b_value != 0:
            print(-1)
            return

        i = 1
        for idx in idxs:
            ans[idx] = replace_val
            if i == b_value:
                # once b_value number of items have been inserted, insert another value
                replace_val += 1
                i = 0
            i += 1

    print(*ans)


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
