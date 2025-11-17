from typing import List


class Solution:
    def kLengthApart(self, nums: List[int], k: int) -> bool:
        if not k:
            return True

        skipped = k
        for num in nums:
            if num:
                if skipped < k:
                    return False
                skipped = 0
            else:
                skipped += 1
        return True
