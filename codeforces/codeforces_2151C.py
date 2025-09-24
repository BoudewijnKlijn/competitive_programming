import bisect
import heapq
import math
import os
from collections import Counter, defaultdict, deque


def solve():
    """Brute force --> TLE
        let k be maximum visitors at one time.
        then allow visitors to enter until k is reached or remaining detections equals visitors inside.
        the next detection must be one of the visitors leaving. it does not matter which visitor.
    ...
    """
    n = int(input())
    a = list(map(int, input().split()))

    ans = list()
    for k in range(1, n + 1):
        q = deque(maxlen=k)
        subtotal = 0
        remaining_detections = 2 * n
        for aa in a:
            if len(q) == k or len(q) == remaining_detections:
                # must be an exit:
                # - maximum visitors reached
                # - or all remaining_detections must be exits
                entry = q.pop()
                subtotal += aa - entry
            else:
                # admit visitor
                q.append(aa)

            remaining_detections -= 1
        ans.append(subtotal)
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
