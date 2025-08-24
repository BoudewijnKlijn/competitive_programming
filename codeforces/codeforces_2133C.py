import os
import sys


def solve():
    """Testing interactive system. Dont know how to solve the problem."""
    n = int(input())
    answer = None
    # while True:
    for _ in range(2):

        if answer is None:
            # make first query
            query = list(range(1, n + 1))
            k = len(query)
            print(f"? {query[0]} {k} {' '.join(map(str, query))}")
        else:
            # use answer in second and later queries
            print(f"? {query[0]} {k} {' '.join(map(str, query))}")

        # flush
        sys.stdout.flush()

        # get answer
        answer = int(input())
        # stop if answer -1
        if answer == -1:
            return

    # give definitive answer
    query = list(range(1, n + 1))
    k = len(query)
    print(f"! {k} {' '.join(map(str, query))}")


if __name__ == "__main__":
    MULTIPLE_TESTS = True

    t = 1
    if MULTIPLE_TESTS:
        t = int(input())

    for _ in range(t):
        solve()
