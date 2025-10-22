from collections import Counter
from typing import List


class Solution:
    def maxFrequency(self, nums: List[int], k: int, numOperations: int) -> int:
        """Identical to 3346.
        286ms Beats 96.77%
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
