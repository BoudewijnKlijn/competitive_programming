from collections import Counter
from typing import List


class Solution:
    def reorderedPowerOf2(self, n: int) -> bool:
        """By reordering, the number of digits and the digits themselves stay the same.
        Try all powers of two, sort string and compare.
        Number of digits has to be the same: verify while power_of_two is less than upper bound.
        Only perform expensive operation if power_of_two is larger than lower bound."""
        digits_n = sorted(str(n))
        lower, upper = n // 10, n * 10  # number of digits has to be the same
        pow2_num = 1
        while pow2_num < upper:
            if lower < pow2_num:
                digits_pow2 = sorted(str(pow2_num))
                if digits_pow2 == digits_n:
                    return True
            pow2_num <<= 1
        return False


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["reorderedPowerOf2"],
        data_file="leetcode_0869_data.txt",
        exclude_data_lines=None,
        repeat=100,
        check_result=True,
    )
