import os
import sys


def get_answer(n: int, s: int) -> int:
    ans = 0
    list_number = [0] + list(
        map(int, list(str(n)))
    )  # Add one extra zero to beginning of number.
    length = len(list_number)
    pos = length - 1  # Start from the most right digit.
    increased = False
    while sum(list_number) > s:
        # Increase digit until its zero. Only way to decrease sum.
        if list_number[pos] > 0:
            multiplier = length - 1 - pos
            ans += (10 - list_number[pos]) * 10**multiplier
            list_number[pos] = 0
            increased = True
        # Also increase one digit to the left with 1. If a 9, keep adding 1 to digits to the left until no longer true.
        if increased:
            while list_number[pos - 1] == 9:
                list_number[pos - 1] = 0
                pos -= 1
            else:
                list_number[pos - 1] += 1
        # Move one digit to the left.
        pos -= 1
    return ans


def solve():
    n, s = map(int, input().split())
    print(get_answer(n, s))


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
