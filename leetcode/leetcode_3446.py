from typing import List


class Solution:
    def sortMatrix(self, grid: List[List[int]]) -> List[List[int]]:
        def walk(grid, diag_length, reverse):
            values = list()
            for r, c in zip(range(0, n), range(n - diag_length, n)):
                if reverse:
                    r, c = c, r
                values.append(grid[r][c])
            values.sort(reverse=reverse)
            for i, (r, c) in enumerate(zip(range(0, n), range(n - diag_length, n))):
                if reverse:
                    r, c = c, r
                grid[r][c] = values[i]
            return grid

        n = len(grid)
        for diag_length in range(1, n):
            grid = walk(grid, diag_length, reverse=False)
        for diag_length in range(n, 0, -1):
            grid = walk(grid, diag_length, reverse=True)

        return grid


if __name__ == "__main__":
    import os

    from timing import timing

    PROBLEM = "3446"
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
        funcs=["sortMatrix"],
        data_file=data_file,
        exclude_data_lines=None,
        check_result=True,
    )
