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

    Between different values of k, many calculations overlap.
    First k visitors are admitted. Then one is let out, and another let in.
    E.g. for both k=1 and k=3, detection 4 is out, and detection 5 is in (assuming n > 3)
        In fact, for k=1 and k=3, all in and out values are the same, except the 2nd and 2nd to last
            which are swapped.
        For k=2 and k=4, all values are the same, except 3rd and 3rd to last, which are swapped.
        Etc.
    """
    n = int(input())
    a = list(map(int, input().split()))

    ans = list()
    for k in range(1, min(n, 2) + 1):
        subtotal = 0
        remaining_detections = 2 * n
        n_visitors = 0
        for aa in a:
            if n_visitors == k or n_visitors == remaining_detections:
                # must be an exit:
                # - maximum visitors reached
                # - or all remaining_detections must be exits
                n_visitors -= 1
                subtotal += aa
            else:
                # admit visitor
                n_visitors += 1
                subtotal -= aa

            remaining_detections -= 1
        ans.append(subtotal)

    # if n > 2, reuse the previous calculations by swapping some values
    # k==3 is the same as k==1, except 2nd detection is admission instead of exit
    #   and a[-2] is exit instead of admission
    # k==5 is the same as k==3, except 4th detection is addmission instead of exit
    #   and a[-4] is exit instead of admission
    # etc.
    # same idea for even values of k
    for k in range(3, n + 1):
        subtotal = ans[-2]
        subtotal -= 2 * a[k - 2]
        subtotal += 2 * a[-(k - 1)]
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
