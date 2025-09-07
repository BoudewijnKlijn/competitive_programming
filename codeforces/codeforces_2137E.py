import os
from collections import Counter


def solve():
    """If there is a single occurence of a number and all numbers below it (from zero) are also single,
    then that numbers and the singles below it, remain unchanged.
    If multiple occurences than they become mex value, and there will be multiple of them in the next pass as well.
    If the smaller numbers occur multiple times, then they become the mex value, which will be higher,
    and in multiple instances, together with other numbers in the second pass, if there is a second pass.
    """
    n, k = list(map(int, input().split()))
    a = list(map(int, input().split()))
    counts = Counter(a)

    # loop over sorted keys. as long as value from 0 onwards only occur once, they dont change.
    key = 0
    constant_sum = 0
    increase_key = True
    single_single_keys = 0
    while True:
        if key not in counts:
            break
        if increase_key and counts[key] == 1:
            single_single_keys += 1
            constant_sum += key
        else:
            increase_key = False

        key += 1

    replace_val = key

    # all values which are higher than key, become key in the first pass
    # then in the next pass they all become key+1 in the next pass. then key thereafter etc.
    ans = constant_sum
    if k % 2 == 1:
        ans += replace_val * (n - single_single_keys)
    else:
        ans += (replace_val + 1) * (n - single_single_keys)
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
