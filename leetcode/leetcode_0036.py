from typing import List


class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:

        columns = [[] for _ in range(9)]
        # check rows and construct columns
        for row in board:
            for i in range(1, 10):
                columns[i - 1].append(row[i - 1])
                if row.count(str(i)) > 1:
                    return False
        # check columns
        for col in columns:
            for i in range(1, 10):
                if col.count(str(i)) > 1:
                    return False
        # check 3x3 boxes
        for i in range(3):
            for j in range(3):
                values = []
                for r in range(3):
                    for c in range(3):
                        values.append(board[i * 3 + r][j * 3 + c])

                for x in range(1, 10):
                    if values.count(str(x)) > 1:
                        return False
        return True


if __name__ == "__main__":
    import os

    from timing import timing

    PROBLEM = "0036"
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
        funcs=["isValidSudoku"],
        data_file=data_file,
        exclude_data_lines=None,
        check_result=True,
    )
