import math
from typing import List


class Solution:
    def triangularSum(self, nums: List[int]) -> int:
        """Use inverse Pascal's triangle.
        The kth element in the nth row (0-indexed) occurs n-1 choose k times --> math.comb(n-1, k).
        """
        n = len(nums)
        ans = 0
        for k in range(n):
            ans += nums[k] * math.comb(n - 1, k)
        return ans % 10


if __name__ == "__main__":
    import os

    from timing import timing

    PROBLEM = "2221"
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
        funcs=["triangularSum"],
        data_file=data_file,
        exclude_data_lines=None,
        check_result=True,
    )
