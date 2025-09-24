import bisect
import heapq
import math
import os
from collections import Counter, defaultdict, deque


def solve():
    n, m = list(map(int, input().split()))
    s = input()
    black_squares = set(map(int, input().split()))

    # print(n, m, s, black_squares)
    positions = [None] + [1] * n

    for i, command in enumerate(s, start=1):
        # execute command for all players
        if command == "A":
            for player in range(i, n + 1):
                positions[player] += 1
            black_squares.add(positions[i])
        else:
            min_first_white = positions[i] + 1
            for player in range(i, n + 1):
                while min_first_white in black_squares:
                    min_first_white += 1
                positions[player] = min_first_white
                if player == i:
                    black_squares.add(positions[i])

    print(len(black_squares))
    print(*sorted(black_squares))


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
