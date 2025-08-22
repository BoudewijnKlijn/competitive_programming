from typing import List


class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        unique = set()
        write_idx = 0
        for num in nums:
            if num in unique:
                continue
            unique.add(num)
            nums[write_idx] = num
            write_idx += 1
        return write_idx
