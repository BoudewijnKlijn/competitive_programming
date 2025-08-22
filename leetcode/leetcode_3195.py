from typing import List


class Solution:
    def minimumArea(self, grid: List[List[int]]) -> int:
        R, C = len(grid), len(grid[0])
        r_min = None
        r_max = 0
        c_min = C
        c_max = 0
        for r in range(R):
            for c in range(C):
                if grid[r][c] == 1:
                    if r_min is None:
                        r_min = r
                    r_max = r
                    c_min = min(c_min, c)
                    c_max = max(c_max, c)
        return (r_max - r_min + 1) * (c_max - c_min + 1)


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["minimumArea"],
        data_file="leetcode_3195_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
