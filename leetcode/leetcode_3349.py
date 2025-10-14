from typing import List


class Solution:
    def hasIncreasingSubarrays(self, nums: List[int], k: int) -> bool:
        """Single loop over nums.
        Check if num increases.
        If 2*k increases in a row, return True.
        If interrupted by a single non-increase where the first and second half
            have at least k increases, also return True.
        """
        prev = nums[0]
        streak = 1
        first_half = False
        for num in nums[1:]:
            if num > prev:
                streak += 1
            else:
                if streak >= k:
                    first_half = True
                else:
                    first_half = False
                streak = 1

            if streak >= 2 * k:
                return True
            elif first_half and streak >= k:
                return True

            prev = num

        return False


if __name__ == "__main__":
    import os

    from timing import timing

    PROBLEM = "3349"
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
        funcs=["hasIncreasingSubarrays"],
        data_file=data_file,
        exclude_data_lines=None,
        check_result=True,
    )
