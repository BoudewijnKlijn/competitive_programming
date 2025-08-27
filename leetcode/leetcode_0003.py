

class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        seen = set()
        left = 0
        ans = 0
        for char in s:
            if char in seen:
                while s[left] != char:
                    seen.remove(s[left])
                    left += 1
                left += 1
            seen.add(char)
            if len(seen) > ans:
                ans = len(seen)
        return ans


if __name__ == "__main__":
    import os

    from timing import timing

    PROBLEM = "0003"
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
        funcs=["lengthOfLongestSubstring"],
        data_file=data_file,
        exclude_data_lines=None,
        check_result=True,
    )
