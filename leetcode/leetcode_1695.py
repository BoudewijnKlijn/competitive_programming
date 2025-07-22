from typing import List


class Solution:
    def maximumUniqueSubarray(self, nums: List[int]) -> int:
        """Two pointers. Sliding window.
        Runtime 175ms
        Beats 94.32%
        """
        subarrayset = set()
        left, right = -1, -1
        ans = 0
        current_sum = 0
        # iterate until all numbers are used
        while right < len(nums) - 1:
            right += 1
            # add numbers if not in subarray yet
            if nums[right] not in subarrayset:
                subarrayset.add(nums[right])
                current_sum += nums[right]
                ans = max(ans, current_sum)
                continue
            # number already in subarray. shrink from the left, until number is out.
            while left < right:
                left += 1
                if nums[left] != nums[right]:
                    subarrayset.remove(nums[left])
                    current_sum -= nums[left]
                else:
                    break
        return ans


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["maximumUniqueSubarray"],
        data_file="leetcode_1695_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
