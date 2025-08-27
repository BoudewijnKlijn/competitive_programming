

class Solution:
    def maxDiff(self, num: int) -> int:
        return self.smarter(num)

    def smarter(self, num: int) -> int:
        """Largest diff is obtained from large diff in most significant digit change.
        Large number: make first non-9 significant digit 9.
        Small number: make first non-1 significant digit 1."""

        def find_and_replace(str_num, replace):
            """Find most significant digit that is not replace, and replace it.
            Number is not allowed to start with one or more leading zeros."""
            for idx, char in enumerate(str_num):
                if replace == 0 and (idx == 0 or str_num[idx] == str_num[0]):
                    # number not allowed to start with one or multiple leading zeros
                    continue
                if char != str(replace):
                    return int(str_num.replace(str_num[idx], str(replace)))

            # no replacement
            return int(str_num)

        str_num = str(num)
        a = find_and_replace(str_num, 9)
        b1 = find_and_replace(str_num, 0)
        b2 = find_and_replace(str_num, 1)
        return max(a - b1, a - b2)

    def bruteforce(self, num: int) -> int:
        """Try all options. Only (10*10)**2 = 10_000 options."""

        def get_replaced(string):
            for x in map(str, range(10)):
                for y in map(str, range(10)):
                    if y == "0" and string[0] == x:
                        # leading zero not allowed
                        continue
                    integer = int(string.replace(x, y))
                    if integer:
                        yield integer

        str_num = str(num)
        ans = 0
        for a in get_replaced(str_num):
            for b in get_replaced(str_num):
                ans = max(ans, abs(a - b))

        return ans


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["maxDiff", "smarter"],
        data_file="leetcode_1432_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
