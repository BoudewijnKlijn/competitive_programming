import heapq
from typing import List


class Solution:
    def maxKelements(self, nums: List[int], k: int) -> int:
        nums = [-n for n in nums]  # we need heap to return maximum instead of minimum
        heapq.heapify(nums)
        ans = 0
        for _ in range(k):
            num = heapq.heappop(nums)
            ans += num
            heapq.heappush(nums, num // 3)  # works because num is negative
        return -ans
