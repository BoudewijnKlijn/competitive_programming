from typing import List


class Solution:
    def isPalindrome(self, s: str) -> bool:
        n = len(s)
        alphabet = set(list("abcdefghijklmnopqrstuvwxyz0123456789"))
        left, right = 0, n - 1
        while left < right:
            while left < right and s[left].lower() not in alphabet:
                left += 1
            lchar = s[left].lower()
            while right > left and s[right].lower() not in alphabet:
                right -= 1
            rchar = s[right].lower()
            if lchar != rchar:
                return False
            left += 1
            right -= 1
        return True


if __name__ == "__main__":
    import os

    from timing import timing

    PROBLEM = "0125"
    data_file = os.path.join(os.path.dirname(__file__), f"leetcode_{PROBLEM}_data.txt")

    # # generate testcases
    # import sys

    # sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    # from generic.helper import InputInteger, InputList, generate_testcases

    # arr1 = InputList(n_min_max=(2, 100_000), val_min_max=(0, 10_000))
    # int1 = InputInteger(val_min_max=(0, 10_000))
    # vars = generate_testcases(structure=(arr1,), n=1, data_file=data_file, solver=None)

    timing(
        solution=Solution(),
        funcs=["isPalindrome"],
        data_file=data_file,
        exclude_data_lines=None,
        check_result=True,
    )
