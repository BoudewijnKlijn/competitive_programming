from collections import Counter
from typing import List


class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        def twosum(numbers, target):
            n = len(numbers)
            left, right = 0, n - 1
            ans = []
            while left < right:
                if numbers[left] + numbers[right] == target:
                    ans.append([numbers[left], numbers[right]])
                    left += 1
                elif numbers[left] + numbers[right] > target:
                    right -= 1
                else:
                    left += 1
            return ans

        # leave at most three of the same
        counts = Counter(nums)
        nums = []
        for k in sorted(counts):
            nums.extend([k] * min(3, counts[k]))

        ans = list()
        seen = set()
        for i, num in enumerate(nums):
            results = twosum(nums[i + 1 :], -num)
            for result in results:
                new = [num, *result]
                if frozenset(new) in seen:
                    continue
                seen.add(frozenset(new))
                ans.append(new)
        return ans


if __name__ == "__main__":
    import os

    from timing import timing

    PROBLEM = "0015"
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
        funcs=["threeSum"],
        data_file=data_file,
        exclude_data_lines=None,
        check_result=True,
    )
