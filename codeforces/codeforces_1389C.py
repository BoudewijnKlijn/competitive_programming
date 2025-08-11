"""Good number means left cyclic and right cyclic are the same.
The set of good numbers seems limited:
- Every number of length 2 is good
- A number of any length with only one and the same digit is good.
- A number with alternating digits where begin and end are not the same.
With that in mind we can construct those numbers and see which one gives the longest number.
"""

import os
import sys
from collections import Counter


def solve():
    string = input().strip()
    length = len(string)
    ans = length - 2
    c = Counter(string)
    max_count = max(c.values())
    if max_count > 2:
        ans = length - max_count
    combinations = [(i, j) for i in range(10) for j in range(10) if i != j]
    for i, j in combinations:
        alternating_sequence_length = 0
        idx = 0
        while True:
            idx = string.find(str(i), idx)
            if idx == -1:
                break
            else:
                alternating_sequence_length += 1
            idx = string.find(str(j), idx)
            if idx == -1:
                alternating_sequence_length -= 1
                break
            else:
                alternating_sequence_length += 1
        if (length - alternating_sequence_length) < ans:
            ans = length - alternating_sequence_length
    print(ans)


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
