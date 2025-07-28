from typing import List


class Solution:
    def countMaxOrSubsets(self, nums: List[int]) -> int:
        """length of nums is at most 16. possible subsets = 2**16 = 65536.
        it's not fast, but it's managable to check all.
        including all numbers will always be equal to max bitwise or."""
        count_max = 0
        max_bitwise_or = self.get_max_bitwise_or(nums)
        n = len(nums)
        for i in range(2**n):
            include_position = bin(i)[2:].zfill(
                n
            )  # whether to include number, yes or no
            bitwise_or = 0
            for do_include, num in zip(map(int, include_position), nums):
                if do_include:
                    bitwise_or |= num

            if bitwise_or == max_bitwise_or:
                count_max += 1

        return count_max

    def get_max_bitwise_or(self, nums):
        bitwise_or = 0
        for n in nums:
            bitwise_or |= n
        return bitwise_or


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["countMaxOrSubsets"],
        data_file="leetcode_2044_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
