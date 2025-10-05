from collections import deque
from typing import List


class Solution:
    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:
        """Reason the other way.
        Go up in height (or equal) and determine to which cells water from Pacific and Atlantic can go.
        Finally determine overlap between sets."""
        R, C = len(heights), len(heights[0])
        DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        pacific = set([(0, c) for c in range(C)]) | set([(r, 0) for r in range(R)])
        atlantic = set([(R - 1, c) for c in range(C)]) | set(
            [(r, C - 1) for r in range(R)]
        )

        def bfs(ocean):
            seen = set()
            q = deque(ocean)
            while q:
                r, c = q.pop()
                if (r, c) in seen:
                    continue
                seen.add((r, c))
                for dr, dc in DIRECTIONS:
                    r2, c2 = r + dr, c + dc
                    if (r2, c2) in seen or r2 < 0 or r2 >= R or c2 < 0 or c2 >= C:
                        continue
                    if heights[r2][c2] >= heights[r][c]:
                        ocean.add((r2, c2))
                        q.append((r2, c2))
            return ocean

        pacific = bfs(pacific)
        atlantic = bfs(atlantic)
        overlap = pacific & atlantic
        return list(overlap)


if __name__ == "__main__":
    import os

    from timing import timing

    PROBLEM = "0417"
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
        funcs=["pacificAtlantic"],
        data_file=data_file,
        exclude_data_lines=None,
        check_result=True,
    )
