import re


class Solution:
    def myAtoi(self, s: str) -> int:
        pattern = r"^\s*[-+]?\d+"
        match = re.match(pattern, s)
        if match:
            ans = int(match.group(0))
        else:
            return 0
        if ans < -(2**31):
            ans = -(2**31)
        elif ans > 2**31 - 1:
            ans = 2**31 - 1
        return ans


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["myAtoi"],
        data_file="leetcode_0008_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
