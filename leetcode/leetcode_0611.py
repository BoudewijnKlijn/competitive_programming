from typing import List


class Solution:
    def triangleNumber(self, nums: List[int]) -> int:
        """A triangle can be made if
        the sum of two shorter sides is greater than the longest side.
        First sort nums.
        Iterate over combinations of the short sides. Check if larger than long side.
        Reuse long side for next iteration for efficiency."""
        ans = 0
        nums.sort()
        n = len(nums)
        for i in range(n - 2):
            k = i + 1
            for j in range(i + 1, n - 1):
                if k < j:
                    k = j
                short_sum = nums[i] + nums[j]
                while k + 1 < n and nums[k + 1] < short_sum:
                    k += 1
                ans += k - j
        return ans


if __name__ == "__main__":
    import os

    from timing import timing

    PROBLEM = "0611"
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
        funcs=["triangleNumber"],
        data_file=data_file,
        exclude_data_lines=None,
        check_result=True,
    )
