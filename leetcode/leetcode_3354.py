from typing import List


class Solution:
    def countValidSelections(self, nums: List[int]) -> int:
        """Difference between sum of positions before and after curr should be <= 1."""
        left_sum = 0
        right_sum = sum(nums)
        ans = 0
        for num in nums:
            if num == 0:
                if 0 <= left_sum - right_sum <= 1:
                    ans += 1
                if 0 <= right_sum - left_sum <= 1:
                    ans += 1
                continue
            left_sum += num
            right_sum -= num
        return ans


if __name__ == "__main__":
    import os

    from timing import timing

    PROBLEM = "3354"
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
        funcs=["countValidSelections"],
        data_file=data_file,
        exclude_data_lines=None,
        check_result=True,
    )
