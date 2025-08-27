import re


class Solution:
    def largestGoodInteger(self, num: str) -> str:
        return self.contains(num)

    def contains(self, num: str) -> str:
        """Faster than regex and one pass.
        Use built in count. Start with largest digit. If count larger than zero, return it.
        """
        for digit in range(9, -1, -1):
            if num.count(str(digit) * 3):
                return str(digit) * 3
        else:
            return ""

    def one_pass(self, num: str) -> str:
        prev = num[0]
        prev_count = 1
        ans = ""
        for char in num[1:]:
            if char == prev:
                prev_count += 1
                if prev_count == 3:
                    ans = max(ans, char * 3)
            else:
                prev = char
                prev_count = 1
        return ans

    def regex(self, num: str) -> str:
        """Regex is faster than one pass over input."""
        pattern = r"(\d)\1\1"  # matches three consecutively identical digits
        result = re.findall(pattern, num)
        if result:
            ans = "0"
            for x in result:
                ans = max(ans, x)
            return ans * 3
        else:
            return ""


if __name__ == "__main__":
    from timing import timing

    def make_test_cases(n):
        import random

        solution = Solution()
        with open("leetcode_2264_data.txt", "a") as fp:
            for _ in range(n):
                out = ""
                for _ in range(1000):
                    out += str(random.randint(0, 9))
                fp.write(f'"{out}"->"{solution.regex(out)}"\n')

    # make_test_cases(10)

    timing(
        solution=Solution(),
        funcs=["regex", "one_pass", "contains", "largestGoodInteger"],
        data_file="leetcode_2264_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
