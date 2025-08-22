from typing import List


class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:
        """Two pointers. One from the right, one from the left.
        Right has to look for non-val, left has to look for val. Then swap.
        Return the number of vals."""
        n = len(nums)
        left, right = 0, n - 1
        n_vals = 0
        while left < right:
            if nums[left] != val:
                left += 1
                continue
            if nums[right] == val:
                right -= 1
                n_vals += 1
                continue

            # swap in place
            nums[left], nums[right] = nums[right], nums[left]
            n_vals += 1
            left += 1
            right -= 1

        return n - n_vals
