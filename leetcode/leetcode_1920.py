from typing import List


class Solution:
    def buildArray(self, nums: List[int]) -> List[int]:
        ans = list()
        for num in nums:
            ans.append(nums[num])
        return ans
