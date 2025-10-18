from typing import List


class Solution:
    def maxDistinctElements(self, nums: List[int], k: int) -> int:
        """Greedy.
        First sort nums.
        Then subtract the largest (or add the smallest) amount such that it is distinct.
        """
        nums.sort()
        ans = 1
        mini = nums[0] - k
        for num in nums[1:]:
            mini += 1
            if num - k > mini:
                mini = num - k
            elif mini > num + k:
                mini -= 1
                continue
            ans += 1
        return ans


if __name__ == "__main__":
    import os

    from timing import timing

    PROBLEM = "3397"
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
        funcs=["maxDistinctElements"],
        data_file=data_file,
        exclude_data_lines=None,
        check_result=True,
    )
