from typing import List


class Solution:
    def longestSubarray(self, nums: List[int]) -> int:
        """First determine the streak of ones and zeros.
        Combine ones to a positive number, same as the length or sum of ones.
        Combine zeros to negative number, abs(number) = equal to length of zeros.
        Thereafter, loop over the streaks. Remember the length of previous streak of ones.
        Reset if value <-1 is encountered. Do nothing when -1. Update previous streak of ones,
            when new positive streak is encountered. Also check if larger than previous max.

        19ms Beats 97.35%"""
        prev = -1 if nums[0] == 0 else 1
        write_pointer = 0
        for num in nums[1:]:
            if num != prev:
                write_pointer += 1
                nums[write_pointer] = 0

            if num == 1:
                nums[write_pointer] += 1
            else:
                nums[write_pointer] -= 1

            prev = num

        # remove everything after write pointer
        nums = nums[: write_pointer + 1]

        # if only zeros or only ones.
        if len(nums) == 1:
            if nums[0] > 0:
                # reduce length by 1
                return nums[0] - 1
            else:
                return 0

        # mix of ones and zeros.
        ans = 0
        prev_streak_ones = None
        for streak in nums:
            if streak < 0:
                if streak < -1:
                    # reset prev streak of ones
                    prev_streak_ones = None
                # do nothing when -1
                continue

            # streak > 0
            if prev_streak_ones is None:
                if streak > ans:
                    ans = streak
            elif streak + prev_streak_ones > ans:
                # combine with prev streak
                ans = streak + prev_streak_ones
            prev_streak_ones = streak
        return ans


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["longestSubarray"],
        data_file="leetcode_1493_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
