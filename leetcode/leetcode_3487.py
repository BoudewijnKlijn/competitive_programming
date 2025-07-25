from typing import List


class Solution:
    def maxSum(self, nums: List[int]) -> int:
        seen = set()
        ans = 0
        for num in nums:
            if num in seen:
                continue
            seen.add(num)
            if num > 0:
                ans += num
        # in case no numbers are positive, return the largest number in seen
        if ans == 0:
            return max(seen)
        return ans


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["maxSum"],
        data_file="leetcode_3487_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
