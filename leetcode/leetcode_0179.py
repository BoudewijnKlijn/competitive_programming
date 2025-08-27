from functools import cmp_to_key
from typing import List


class Solution:
    def largestNumber(self, nums: List[int]) -> str:
        return self.first(nums)

    def first(self, nums: List[int]) -> str:
        # when comparing 34, 30, and 3, 3 should be seen as 33. repeat the characters
        if all(n == 0 for n in nums):
            return "0"
        strings = list(map(str, nums))
        max_digits = 12  # this had to be increased beyond 9 to solve later test cases
        repeated = {old: (old * max_digits) for old in strings}
        strings.sort(reverse=True, key=repeated.__getitem__)
        return "".join(strings)

    def improved(self, nums: List[int]) -> str:
        """Leetcode solution."""
        if all(n == 0 for n in nums):
            return "0"
        sorted_strings = sorted(map(str, nums), reverse=True, key=cmp_to_key(self.cmp))
        return "".join(sorted_strings)

    def cmp(self, x, y):
        return -1 if x + y < y + x else 1


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["first", "improved"],
        data_file="leetcode_0179_data.txt",
        exclude_data_lines=None,
        check_result=True,
        repeat=1000,
    )
