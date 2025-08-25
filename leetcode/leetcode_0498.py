from typing import List


class Solution:
    def findDiagonalOrder(self, mat: List[List[int]]) -> List[int]:
        def get_direction():
            while True:
                yield -1, 1
                yield 1, -1

        R, C = len(mat), len(mat[0])
        r, c = 0, 0
        direction = get_direction()
        dr, dc = next(direction)
        ans = []
        while len(ans) < R * C:
            if 0 <= r < R and 0 <= c < C:
                ans.append(mat[r][c])
                course_corrected = False
            elif not course_corrected:
                # one move to the right when outside matrix
                c += 1
                course_corrected = True
                # go one step further away from matrix, to prevent skipping a number
                r, c = r + dr, c + dc
                dr, dc = next(direction)
            r, c = r + dr, c + dc
        return ans


if __name__ == "__main__":
    import os

    from timing import timing

    PROBLEM = "0498"
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
        funcs=["findDiagonalOrder"],
        data_file=data_file,
        exclude_data_lines=None,
        check_result=True,
    )
