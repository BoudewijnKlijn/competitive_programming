from typing import List


class Solution:
    def getSneakyNumbers(self, nums: List[int]) -> List[int]:
        seen = set()
        ans = list()
        for num in nums:
            if num in seen:
                ans.append(num)
            seen.add(num)
        return ans
