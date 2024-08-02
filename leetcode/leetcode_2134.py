from typing import List


class Solution:
    def minSwaps(self, nums: List[int]) -> int:
        n1 = sum(nums)
        sum_range = max_sum_range = sum(nums[:n1])
        for remove, add in zip(nums, nums[n1:] + nums[:n1]):
            sum_range += add - remove
            if sum_range > max_sum_range:
                max_sum_range = sum_range
        return n1 - max_sum_range
