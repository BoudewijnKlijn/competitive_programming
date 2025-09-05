from collections import Counter
from typing import List


class Solution:
    def deleteAndEarn(self, nums: List[int]) -> int:
        return self.use_counter(nums)

    def use_counter(self, nums: List[int]) -> int:
        counts = Counter(nums)
        sorted_items = sorted(counts.items())
        n = len(sorted_items)
        dp = [0] * n
        prev_key = None
        for i, (k, v) in enumerate(sorted_items):
            if prev_key is None:
                dp[i] = k * v
            elif k - prev_key == 1:
                if i == 1:
                    dp[i] = max(dp[i - 1], k * v)
                else:
                    dp[i] = max(dp[i - 1], k * v + dp[i - 2])
            else:
                dp[i] = dp[i - 1] + k * v
            prev_key = k
        return dp[-1]

    def complete_number_line(self, nums: List[int]) -> int:
        MAX = 10_001
        counts = [0] * MAX
        for num in nums:
            counts[num] += 1

        dp = [0] * MAX
        dp[1] = counts[1]
        for i in range(2, MAX):
            dp[i] = max(i * counts[i] + dp[i - 2], dp[i - 1])
        return dp[-1]


if __name__ == "__main__":
    import os

    from timing import timing

    PROBLEM = "0740"
    data_file = os.path.join(os.path.dirname(__file__), f"leetcode_{PROBLEM}_data.txt")

    # # generate testcases
    # import sys

    # sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    # from generic.helper import InputInteger, InputList, generate_testcases

    # arr1 = InputList(n_min_max=(2, 100_000), val_min_max=(0, 10_000))
    # int1 = InputInteger(val_min_max=(0, 10_000))
    # vars = generate_testcases(structure=(arr1,), n=1, data_file=data_file, solver=None)

    timing(
        solution=Solution(),
        funcs=["complete_number_line", "use_counter"],
        data_file=data_file,
        exclude_data_lines=None,
        check_result=True,
    )
