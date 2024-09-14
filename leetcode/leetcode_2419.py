from typing import List


class Solution:
    def longestSubarray(self, nums: List[int]) -> int:
        # maximum bitwise AND is just the highest number
        # the longest subarray is a repetition of that number
        max_num = 0
        for n in nums:
            if n > max_num:
                max_num = n
                max_len = 1
                counter = 1
            elif n == max_num and n == prev:
                counter += 1
                if counter > max_len:
                    max_len = counter
            elif n == max_num:
                counter = 1
            else:
                counter = 0
            prev = n
        return max_len


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["longestSubarray"],
        data_file="leetcode_2419_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
