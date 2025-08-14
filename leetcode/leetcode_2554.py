from typing import List


class Solution:
    def maxCount(self, banned: List[int], n: int, maxSum: int) -> int:
        banned = set(banned)
        total = 0
        ans = 0
        for i in range(1, n + 1):
            if i in banned:
                continue
            total += i
            ans += 1
            if total > maxSum:
                return ans - 1
        return ans
