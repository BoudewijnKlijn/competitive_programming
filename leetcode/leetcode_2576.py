from typing import List


class Solution:
    def maxNumOfMarkedIndices(self, nums: List[int]) -> int:
        """Maximum ans is n, matching all.
        First sort nums.
        Then if some n[i]*2 <= n[j], and i<j, then also for every k>j.
        Use two pointers. Both moving to the left. Right starts at the largest number.
            Left starts halfway.
        If left would start more to the right, we might use a large number as a small number
            and be left with many small numbers which cannot be marked, because the small numbers
            are too small to be used as a large number.
        If left starts more to the left, we possibly have too few numbers on the left to match
            numbers on the right.
        If left is too large to be used as a small number, then starting left more to the right
            would not have solved that.
        """
        nums.sort()
        n = len(nums)
        left, right = n // 2 - 1, n - 1
        ans = 0
        while left >= 0:
            if 2 * nums[left] <= nums[right]:
                ans += 2
                left -= 1
                right -= 1
            else:
                left -= 1
        return ans


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["maxNumOfMarkedIndices"],
        data_file="leetcode_2576_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
