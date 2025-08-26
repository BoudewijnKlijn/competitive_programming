from typing import List


class Solution:
    def rotate(self, matrix: List[List[int]]) -> None:
        """
        Do not return anything, modify matrix in-place instead.

        The first column in reverse becomes the first row.
        The second column in reverse becomes the second row.
        Etc.
        """
        copy = [[val for val in row] for row in matrix]
        # reverses rows and then rezips to get columns
        for r, column in enumerate(zip(*copy[::-1])):
            for c, val in enumerate(column):
                matrix[r][c] = val
        # return matrix


if __name__ == "__main__":
    import os

    from timing import timing

    PROBLEM = "0048"
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
        funcs=["rotate"],
        data_file=data_file,
        exclude_data_lines=None,
        check_result=True,
    )
