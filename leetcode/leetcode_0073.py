from typing import List


class Solution:
    def setZeroes(self, matrix: List[List[int]]) -> None:
        """
        Do not return anything, modify matrix in-place instead.
        """
        m, n = len(matrix), len(matrix[0])
        tmp = matrix.copy()
        for r, row in enumerate(matrix):
            if 0 in set(row):
                matrix[r] = [0] * n
        for c, col in enumerate(zip(*tmp)):
            if 0 in set(col):
                for r in range(m):
                    tmp[r][c] = 0
        return matrix


if __name__ == "__main__":
    import os

    from timing import timing

    PROBLEM = "0073"
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
        funcs=["setZeroes"],
        data_file=data_file,
        exclude_data_lines=None,
        check_result=True,
    )
