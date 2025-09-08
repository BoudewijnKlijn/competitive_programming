from typing import List


class Solution:
    def uniquePathsWithObstacles(self, obstacleGrid: List[List[int]]) -> int:
        m, n = len(obstacleGrid), len(obstacleGrid[0])
        dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]

        # terminal value obstructed or not?
        if obstacleGrid[m - 1][n - 1] == 1:
            return 0
        else:
            dp[m - 1][n - 1] = 1

        for row in range(m - 1, -1, -1):
            for col in range(n - 1, -1, -1):
                if row == m - 1 and col == n - 1:
                    # skip terminal value
                    continue
                if obstacleGrid[row][col] == 1:
                    # skip obstacles
                    continue
                dp[row][col] = dp[row + 1][col] + dp[row][col + 1]
        return dp[0][0]


if __name__ == "__main__":
    import os

    from timing import timing

    PROBLEM = "0063"
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
        funcs=["uniquePathsWithObstacles"],
        data_file=data_file,
        exclude_data_lines=None,
        check_result=True,
    )
