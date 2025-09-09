import heapq
import os
import sys
from collections import Counter, defaultdict, deque


def solve():
    """Alice wants to maximize, Bob wants to minimize.
    Result is cost + alternating sum of array.
    In a turn they can end the game or they can swap two values, which increases the cost.
    It is optimal for Alice if this is the maximum value she can achieve. Either because
        it is the absolute maximum or because it will decrease if she doesn't end.
    Vice versa for bob: End if absolute minimum or if it will increase if not end now.
    Swapping adds r-l (indices) to cost, so is in favor of Alice.
        Alice would want to swap a large value with high odd (0-indexed) index with a
        small value with low even (0-indexed). This increases sum and increases cost most.
    Bob can always undo the move of Alice. Alice can always undo the move of Bob.
        This is advantageous for Alice, because costs keep increasing. Therefore Bob will always
        terminate immediately.
        Alice only terminates immediately if swapping reduces the sum.
    Just need to determine if swapping once any two numbers increases the total value...
        Added value from swapping depends on left and right value and left and right index.


    .... could not figure out how to compute cost efficienctly......
    """
    input = sys.stdin.readline
    _ = int(input().strip())
    a = list(map(int, input().strip().split()))

    total = 0
    even = True
    best_even_right = None
    best_even_left = None
    best_odd_right = None
    best_odd_left = None
    max_cost_left = None  # maximize
    max_cost_right = None  # maximize
    for i, aa in enumerate(a):
        if even:
            mult = 1

            # even_right_cost_change = i - 2 * aa
            # if best_even_right is None or best_even_right > even_right_cost_change:
            #     best_even_right = even_right_cost_change
            # even_left_cost_change = -i - 2 * aa
            # if best_even_left is None or best_even_left > even_left_cost_change:
            #     best_even_left = even_left_cost_change
        else:
            mult = -1

            # odd_left_cost_change = -i + 2 * aa
            # if best_odd_left is None or best_odd_left > odd_left_cost_change:
            #     best_odd_left = odd_left_cost_change
            # odd_right_cost_change = i + 2 * aa
            # if best_odd_right is None or best_odd_right > odd_right_cost_change:
            #     best_odd_right = odd_right_cost_change

        total += mult * aa

        # maximize left and right cost part
        cost_left = aa * mult * -2 - i
        if max_cost_left is None or cost_left > max_cost_left:
            max_cost_left = cost_left
        cost_right = aa * mult * -2 + i
        if max_cost_right is None or cost_right > max_cost_right:
            max_cost_right = cost_right

        # # using this value to swap
        # even_right_cost_change = i - 2 * aa
        # if best_even_right is None or best_even_right > even_right_cost_change:
        #     best_even_right = even_right_cost_change
        # even_left_cost_change = -i - 2 * aa
        # if best_even_left is None or best_even_left > even_left_cost_change:
        #     best_even_left = even_left_cost_change

        even = not even
    cost = max_cost_left + max_cost_right

    # cost = max(best_odd_left + best_even_right, best_even_left + best_odd_right)
    # increase of total from optimal swap
    print(total, cost, total + cost)
    # if cost > 0:
    #   print(total, cost, total + cost)
    # else:
    #     print(total)


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
