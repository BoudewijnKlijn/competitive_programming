"""A number is divisible by 8 if the last 3 digits are divisible by 8 or are 000
https://www.cuemath.com/numbers/divisibility-rule-of-8/"""

import os
import re


def solve():
    str_number = input()

    def make_pattern(number):
        return ".*".join([f"({d})" for d in str(number)])

    numbers_div_by_8 = [n for n in range(1000) if n % 8 == 0]

    def div_by_8(string):
        if "0" in string:
            return "YES\n0"
        for n in numbers_div_by_8:
            pattern = make_pattern(n)
            if re.search(pattern, string):
                return f"YES\n{n}"
        return "NO"

    print(div_by_8(str_number))


if __name__ == "__main__":
    MULTIPLE_TESTS = False
    if not os.path.exists("LOCAL"):
        t = 1
        if MULTIPLE_TESTS:
            t = int(input())
        for _ in range(t):
            solve()
    else:
        import test_runner

        test_runner.main(solve, __file__, MULTIPLE_TESTS)
