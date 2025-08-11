import os
import sys


def is_solvable_v3(n, a, b):
    """Smart way: Analyze numbers in modulo form.
    If remainder goal is 1, we can just keep adding b to get to n.
    Otherwise, make more remainders from starting point (which is 1).
    Adding b doesn't change the remainder (since we do mod b). Multiplying with a might change the remainder.
    """
    remainder_goal = n % b
    number = 1
    remainders_checked = set()
    while True:
        remainder = number % b
        if remainder_goal == remainder:
            return True
        if remainder in remainders_checked:
            return False
        else:
            remainders_checked.add(remainder)
        number *= a
        if number > n:
            return False


def solve():
    n, a, b = map(int, input().split())
    if is_solvable_v3(n, a, b):
        print("Yes")
    else:
        print("No")


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
