from collections import deque
from typing import List


class Solution:
    def rotate(self, nums: List[int], k: int) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        n = len(nums)
        tmp = deque(nums[n - k % n :])
        for i in range(n):
            tmp.append(nums[i])
            nums[i] = tmp.popleft()
