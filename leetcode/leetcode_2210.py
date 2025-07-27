from typing import List


class Solution:
    def countHillValley(self, nums: List[int]) -> int:
        # remove equal neighbors
        new_nums = [nums[0]]
        for num in nums[1:]:
            if num == new_nums[-1]:
                continue
            new_nums.append(num)

        # check for hills and valleys
        ans = 0
        for left, num, right in zip(new_nums, new_nums[1:], new_nums[2:]):
            if left < num > right:  # hill
                ans += 1
            elif left > num < right:  # valley
                ans += 1
        return ans


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["countHillValley"],
        data_file="leetcode_2210_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
