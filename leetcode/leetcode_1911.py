from typing import List


class Solution:
    def maxAlternatingSum(self, nums: List[int]) -> int:
        """At any stage, we can choose to take or not take the number.
        If length of numbers taken is even, the number is added. If odd, number is subtracted.
        Keep maximum of even and odd length.
        """
        sums = (0, 0)  # (even, odd)
        for num in nums:
            # (even + don't take = even, odd + take (subtract num) = even)
            # (odd + don't take = odd, even + take (add num) = odd)
            sums = (max(sums[0], sums[1] - num), max(sums[1], sums[0] + num))
        return max(sums)


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["maxAlternatingSum"],
        data_file="leetcode_1911_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
