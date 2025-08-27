from typing import List


class Solution:
    def maxArea(self, height: List[int]) -> int:
        """Use two pointers. Move the one of the lowest bar.
        Both pointers reduce width by one when moving left or right.
        Since height is min of both, moving the heighest pointer would never increase the
            minimum height, while moving the lowest is guaranteed not to lower it. It is thus
            best to always move the lowest height pointer.
        """
        left, right = 0, len(height) - 1
        ans = min(height[left], height[right]) * (right - left)
        while left < right:
            if height[left] < height[right]:
                left += 1
            else:
                right -= 1
            area = min(height[left], height[right]) * (right - left)
            ans = max(ans, area)
        return ans


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["maxArea"],
        data_file="leetcode_0009_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
