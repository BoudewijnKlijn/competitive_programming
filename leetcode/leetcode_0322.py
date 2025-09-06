from functools import cache
from typing import List


class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        return self.using_tabulation(coins, amount)

    def using_tabulation(self, coins: List[int], amount: int) -> int:
        """Faster, and less memory.
        270ms Beats 99.18%"""
        coins.sort()
        INF = amount + 1
        dp = [0] + [INF] * amount
        for i in range(1, amount + 1):
            best = INF
            for coin in coins:
                if coin > i:
                    break
                val = 1 + dp[i - coin]
                if val < best:
                    best = val
            dp[i] = best

        ans = dp[amount]
        return -1 if ans == INF else ans

    def using_recursion(self, coins: List[int], amount: int) -> int:
        """Accepted, but not fast.
        747ms Beats 62.70%
        """

        @cache
        def inner(amount):
            if amount == 0:
                return 0

            best = [float("inf")]
            for coin in coins:
                if amount >= coin:
                    best.append(1 + inner(amount - coin))
            return min(best)

        ans = inner(amount)
        return -1 if ans == float("inf") else ans


# +-------------------+--------------------+
# |   using_recursion |   using_tabulation |
# |-------------------+--------------------|
# |          0.000026 |           0.000006 |
# |          0.000007 |           0.000002 |
# |          0.000004 |           0.000001 |
# |          0.000793 |           0.000280 |
# |          0.000635 |           0.000196 |
# |          0.000995 |           0.000343 |
# |          0.002862 |           0.000374 |
# |          0.000647 |           0.000273 |
# +-------------------+--------------------+


if __name__ == "__main__":
    import os

    from timing import timing

    PROBLEM = "0322"
    data_file = os.path.join(os.path.dirname(__file__), f"leetcode_{PROBLEM}_data.txt")

    # generate testcases
    import sys

    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from generic.helper import InputInteger, InputList, generate_testcases

    arr1 = InputList(n_min_max=(12, 12), val_min_max=(1, 50))
    int1 = InputInteger(val_min_max=(0, 1_000))
    # vars = generate_testcases(
    #     structure=(arr1, int1),
    #     n=5,
    #     data_file=data_file,
    #     solver=Solution().using_tabulation,
    # )

    timing(
        solution=Solution(),
        funcs=["using_recursion", "using_tabulation"],
        data_file=data_file,
        exclude_data_lines=None,
        check_result=True,
    )
