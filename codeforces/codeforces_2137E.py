import os
from collections import Counter
from math import prod


def solve():
    n, k = list(map(int, input().split()))
    a = list(map(int, input().split()))

    def inner(counts_a):
        # get first value that is not present in a
        replace_val = 0
        while replace_val in counts_a:
            replace_val += 1

        # build new counter.
        # all values more than replace_val or occur more than once get replaced by replace_val
        new_a = dict()
        n_added = 0
        for key in range(replace_val):
            if key in counts_a and counts_a[key] == 1:
                new_a[key] = 1
                n_added += 1
        new_a[replace_val] = n - n_added
        return new_a

    # run solver a few times. a loop will establish or all values are the same.
    history = list()
    counts_a = Counter(a)
    while k > 0 and len(history) < 3:
        counts_a = inner(counts_a)
        history.append(sum(map(prod, counts_a.items())))
        k -= 1

    # return answer based on whether k == 0 or odd or even.
    if k == 0 or k % 2 == 0:
        print(history[-1])
    else:
        print(history[-2])


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
