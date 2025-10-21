from collections import Counter
from typing import List


class Solution:
    def maxFrequency(self, nums: List[int], k: int, numOperations: int) -> int:
        """Each index can only be operated on once.
        It's possible not all indices are operated on. (if numOperations < n)
        Not required to return which specific value has max frequency.
        It may be useful to sort nums and/or to count frequencies of nums.
        Numbers which are further apart than 2*k can never become the same number.
        If sorted, maybe possible to use two pointers/ window.
            Increase window as long as <= 2*k and <= numOperations (and subtract one freq possibly)
        352ms Beats 90.12%
        """
        nums.sort()
        n = len(nums)
        two_k = 2 * k
        ans = 0
        left = 0
        # option one: only look at the range, assume everything needs to be adjusted
        for right in range(n):
            while nums[left] < nums[right] - two_k:
                left += 1
            freq = right - left + 1
            if freq > ans:
                ans = freq
        if ans > numOperations:
            ans = numOperations

        # option two: look at specific value. some values don't need to be adjusted
        counter = Counter(nums)
        left = 0
        right = 0
        for i in range(n):
            exact_freq = counter[nums[i]]
            while right < n - 1 and nums[right + 1] <= nums[i] + k:
                right += 1
            while nums[left] < nums[i] - k:
                left += 1
            freq = right - left + 1
            if freq > numOperations + exact_freq:
                freq = numOperations + exact_freq
            if freq > ans:
                ans = freq

        return ans


if __name__ == "__main__":
    import os

    from timing import timing

    PROBLEM = "3346"
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
        funcs=["maxFrequency"],
        data_file=data_file,
        exclude_data_lines=None,
        check_result=True,
    )
