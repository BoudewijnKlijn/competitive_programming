import os
import sys


def solve():
    n = int(input())
    a = list(map(int, input().split()))
    max_number = None
    current_time = 0
    for i, ai in enumerate(a):
        if max_number is None:
            max_number = ai
            continue
        elif ai > max_number:
            max_number = ai
        difference_with_max_number_before = ai - max_number
        # If larger number before we have to increase time.
        # Can subtract increments that were used for others. Sum of all previous is current one minus 1, due to
        # increments with power of 2.
        difference_with_max_number_before += 2**current_time - 1
        while difference_with_max_number_before < 0:
            current_time += 1
            difference_with_max_number_before += 2 ** (current_time - 1)
    # Answer.
    print(current_time)


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
