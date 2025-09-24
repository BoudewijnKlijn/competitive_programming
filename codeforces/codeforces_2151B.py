import bisect
import heapq
import math
import os
from collections import Counter, defaultdict, deque


def solve():
    """Only the coloring of the final cell _might_ change what the next player does.
    So, consider the next player being on the position of the player before him, before its last move.
    Then execute the second last and last command.
    """
    n, m = list(map(int, input().split()))
    commands = input()
    black_squares = set(map(int, input().split()))

    positions = [None] + [1] * n
    pos = 1
    prev_command = None
    for player in range(1, n + 1):
        # correction for if previous last command is B
        # the next (this) player would move to another cell.
        if prev_command == "B":
            while pos in black_squares:
                pos += 1

        # now execute the extra command for the current player.
        command = commands[player - 1]
        pos += 1
        if command == "B":
            while pos in black_squares:
                pos += 1
        positions[player] = pos
        black_squares.add(pos)
        prev_command = command

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
