from typing import List


class Solution:
    def reverse(self, x: int) -> int:
        is_negative = True if x < 0 else False

        x = abs(x)
        new = 0
        while x > 0:
            x, remainder = divmod(x, 10)
            new = new * 10 + remainder

        ans = -new if is_negative else new
        if -(2**31) <= ans <= 2**31 - 1:
            return ans
        return 0


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["reverse"],
        data_file="leetcode_0007_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
