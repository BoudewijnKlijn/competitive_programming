from typing import List


class Solution:
    def rob(self, nums: List[int]) -> int:
        nums = [0, 0] + nums
        n = len(nums)
        dp = [0] * n
        for i, num in enumerate(nums[2:], start=2):
            dp[i] = num + max(dp[: i - 1])
        return max(dp[-2:])


if __name__ == "__main__":
    import os

    from timing import timing

    PROBLEM = "0198"
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
        funcs=["rob"],
        data_file=data_file,
        exclude_data_lines=None,
        check_result=True,
    )
