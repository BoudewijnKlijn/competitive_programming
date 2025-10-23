import math
from typing import List


class Solution:
    def hasSameDigits(self, nums: List[int]) -> int:
        """This problem can reuse solution of problem 2221."""

        def problem_2221(nums):
            n = len(nums)
            ans = 0
            for k in range(n):
                ans += nums[k] * math.comb(n - 1, k)
            return ans % 10

        nums = list(map(int, nums))
        one, two = problem_2221(nums[:-1]), problem_2221(nums[1:])
        return one == two


if __name__ == "__main__":
    import os

    from timing import timing

    PROBLEM = "3461"
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
        funcs=["hasSameDigits"],
        data_file=data_file,
        exclude_data_lines=None,
        check_result=True,
    )
