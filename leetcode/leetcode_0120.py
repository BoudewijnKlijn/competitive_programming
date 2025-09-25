from typing import List


class Solution:
    def minimumTotal(self, triangle: List[List[int]]) -> int:
        n = len(triangle)

        for row in reversed(range(n - 1)):
            for col in range(row + 1):
                triangle[row][col] += min(
                    triangle[row + 1][col], triangle[row + 1][col + 1]
                )
        return triangle[0][0]


if __name__ == "__main__":
    import os

    from timing import timing

    PROBLEM = "0120"
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
        funcs=["minimumTotal"],
        data_file=data_file,
        exclude_data_lines=None,
        check_result=True,
    )
