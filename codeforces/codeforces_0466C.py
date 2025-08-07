import os
from itertools import accumulate


def solve():
    """Determine running sum.
    When it hits 1/3 or 2/3 of total that is one possible option to split.
    Finally take product of number of 1/3 and 2/3 splits.
    If total==0, count number of times cumsum==0 and subtract 2 for start and end.
        Then apply pascals triangle."""
    _ = int(input())
    arr = list(map(int, input().split()))
    total = sum(arr)
    if total % 3 != 0:
        print(0)
        return

    sum_part = total // 3
    ans = 0
    if sum_part == 0:
        # count number of times cumulative sum is zero
        cumsum_zero = sum(x == 0 for x in accumulate(arr))
        # subtract two for zero at start and end
        if cumsum_zero > 2:
            cumsum_zero -= 2
            ans = cumsum_zero * (cumsum_zero + 1) // 2
    else:
        one_third = list()
        two_third = list()
        for cumsum in accumulate(arr):
            if cumsum == sum_part:
                one_third.append(1)
                two_third.append(0)
            elif cumsum == 2 * sum_part:
                one_third.append(0)
                two_third.append(1)

        # match all one_thirds with two_thirds that come __after__ it
        two_third_cumsum = list(accumulate(two_third))
        for i, x in enumerate(one_third):
            if not x:
                continue
            ans += two_third_cumsum[-1] - two_third_cumsum[i]
    print(ans)


if __name__ == "__main__":
    MULTIPLE_TESTS = False

    if not os.path.exists("LOCAL"):
        t = 1
        if MULTIPLE_TESTS:
            t = int(input())

        for i in range(t):
            solve()
    else:
        import test_runner

        test_runner.main(solve, __file__, MULTIPLE_TESTS)
