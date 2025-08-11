import os
import sys


def solve():
    n = int(input())
    s = list(map(int, input().strip()))
    subsequences = [0] * n
    max_subsequence = 0
    last_used_zero = list()
    last_used_one = list()
    for i, char in enumerate(s):
        if char == 0:
            try:
                subsequence = last_used_one.pop()
            except IndexError:
                subsequence = max_subsequence + 1
                max_subsequence += 1
            last_used_zero.append(subsequence)
        elif char == 1:
            try:
                subsequence = last_used_zero.pop()
            except IndexError:
                subsequence = max_subsequence + 1
                max_subsequence += 1
            last_used_one.append(subsequence)
        else:
            raise ValueError()
        subsequences[i] = subsequence
    print(max(subsequences))
    print(" ".join(map(str, subsequences)))


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
