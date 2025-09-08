from typing import List


class Solution:
    def minPathSum(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        INF = 200 * m * n + 1
        dp = [[None for _ in range(n + 1)] for _ in range(m + 1)]

        # set terminal value, and values for outside grid
        dp[m - 1][n - 1] = grid[m - 1][n - 1]
        dp[m] = [INF] * (n + 1)  # outside grid, bottom row
        for row in range(m + 1):
            dp[row][n] = INF  # outside grid, rightmost col

        for row in range(m - 1, -1, -1):
            for col in range(n - 1, -1, -1):
                if dp[row][col] is not None:
                    # skip if terminal square
                    continue
                dp[row][col] = grid[row][col] + min(dp[row + 1][col], dp[row][col + 1])
        return dp[0][0]


if __name__ == "__main__":
    import os

    from timing import timing

    PROBLEM = "0064"
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
        funcs=["minPathSum"],
        data_file=data_file,
        exclude_data_lines=None,
        check_result=True,
    )
