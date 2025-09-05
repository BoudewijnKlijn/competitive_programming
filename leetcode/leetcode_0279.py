class Solution:
    def numSquares(self, n: int) -> int:
        perfect_squares = [i**2 for i in range(101)]
        dp = [n] * (n + 1)
        dp[0] = 0
        for i in range(n + 1):
            for ps in perfect_squares:
                if ps + i > n:
                    break
                dp[ps + i] = min(dp[i] + 1, dp[ps + i])
        return dp[n]


if __name__ == "__main__":
    import os

    from timing import timing

    PROBLEM = "0279"
    data_file = os.path.join(os.path.dirname(__file__), f"leetcode_{PROBLEM}_data.txt")

    # # generate testcases
    # import sys

    # sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    # from generic.helper import InputInteger, generate_testcases

    # int1 = InputInteger(val_min_max=(1, 10_000))
    # generate_testcases(
    #     structure=(int1,), n=10, data_file=data_file, solver=Solution().numSquares
    # )

    timing(
        solution=Solution(),
        funcs=["numSquares"],
        data_file=data_file,
        exclude_data_lines=None,
        check_result=True,
    )
