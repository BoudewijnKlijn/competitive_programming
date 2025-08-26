from itertools import cycle
from typing import List


class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        def get_direction():
            for dr, dc in cycle([(0, 1), (1, 0), (0, -1), (-1, 0)]):
                yield dr, dc

        R, C = len(matrix), len(matrix[0])
        direction = get_direction()

        visited = set([(0, 0)])
        r, c = 0, 0
        dr, dc = next(direction)
        ans = [matrix[r][c]]
        while len(visited) < R * C:
            while (
                (r + dr, c + dc) in visited
                or r + dr < 0
                or r + dr >= R
                or c + dc < 0
                or c + dc >= C
            ):
                dr, dc = next(direction)

            r += dr
            c += dc
            ans.append(matrix[r][c])
            visited.add((r, c))
        return ans


if __name__ == "__main__":
    import os

    from timing import timing

    PROBLEM = "0054"
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
        funcs=["spiralOrder"],
        data_file=data_file,
        exclude_data_lines=None,
        check_result=True,
    )
