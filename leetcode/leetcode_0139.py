from functools import cache
from typing import List


class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        return self.tabulation(s, wordDict)

    def tabulation(self, s: str, wordDict: List[str]) -> bool:
        n = len(s)
        wordDict = set(wordDict)
        dp = [False] * n + [True]
        for start in range(n - 1, -1, -1):
            for end in range(n - 1, start - 1, -1):
                if not dp[end + 1]:
                    # immediate continuation.
                    # if this word matches, then from character after end, we should be
                    # able to reach another word or the end. if not, cannot set dp[start] to true.
                    # instead of checking everytime we find a word, do check immediately.
                    continue
                if s[start : end + 1] in wordDict:
                    dp[start] = True
                    # early stopping
                    break
        return dp[0]

    def recursion(self, s: str, wordDict: List[str]) -> bool:
        @cache
        def inner(s):
            if not s:
                return True

            n = len(s)
            ans = False
            for end in range(1, n + 1):
                if s[:end] in wordDict and inner(s[end:]):
                    ans = True
            return ans

        wordDict = set(wordDict)
        return inner(s)


if __name__ == "__main__":
    import os

    from timing import timing

    PROBLEM = "0139"
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
        funcs=["recursion", "tabulation"],
        data_file=data_file,
        exclude_data_lines=None,
        check_result=True,
    )
