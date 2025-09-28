from typing import List


class Solution:
    def largestPerimeter(self, nums: List[int]) -> int:
        """The long side must be less than sum of short sides to be a triangle.
        Max perimeter results from largest sides."""
        nums.sort(reverse=True)
        n = len(nums)
        for long_side in range(n - 2):
            sum_short = nums[long_side + 1] + nums[long_side + 2]
            if nums[long_side] < sum_short:
                return nums[long_side] + sum_short
        else:
            return 0


if __name__ == "__main__":
    import os

    from timing import timing

    PROBLEM = "0976"
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
        funcs=["largestPerimeter"],
        data_file=data_file,
        exclude_data_lines=None,
        check_result=True,
    )
