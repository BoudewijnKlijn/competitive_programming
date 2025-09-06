from functools import cache
from typing import List


class Solution:
    def mostPoints(self, questions: List[List[int]]) -> int:
        return self.using_dp(questions)

    def using_dp(self, questions: List[List[int]]) -> int:
        """Tabulation from the end.
        Accepted."""
        n = len(questions)
        dp = [0] * n
        for i in range(n - 1, -1, -1):
            points, brainpower = questions[i]
            extra = 0
            if i + brainpower + 1 <= n - 1:
                extra = dp[i + brainpower + 1]
            alternative = 0
            if i + 1 <= n - 1:
                alternative = dp[i + 1]
            dp[i] = max(points + extra, alternative)
        return dp[0]

    def using_recursion(self, questions: List[List[int]]) -> int:
        """Without cache: Time Limit Exceeded. 14 / 54 testcases passed.
        With cache: Memory Limit Exceeded. 48 / 54 testcases passed.
        """

        @cache
        def inner(questions):
            if not questions:
                return 0

            return max(
                questions[0][0] + inner(questions[questions[0][1] + 1 :]),
                inner(questions[1:]),
            )

        questions = tuple(map(tuple, questions))
        return inner(questions)


if __name__ == "__main__":
    import os

    from timing import timing

    PROBLEM = "2140"
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
        funcs=[
            "using_dp",
            "using_recursion",
        ],
        data_file=data_file,
        exclude_data_lines=[3],
        check_result=True,
    )
