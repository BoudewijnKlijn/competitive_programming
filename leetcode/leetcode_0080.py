from typing import List


class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        once = set()
        twice = set()
        write_idx = 0
        for num in nums:
            if num in once:
                if num in twice:
                    continue
                twice.add(num)
            once.add(num)
            nums[write_idx] = num
            write_idx += 1
        return write_idx
