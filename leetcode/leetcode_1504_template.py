from typing import List


class Solution:
    def numSubmat(self, mat: List[List[int]]) -> int:
        """Divide rectangles into several groups: 1x1, mx1, 1xn and mxn.
            Call 1x1: singles, and mx1 and 1xn: bars.
        The singles can be counted immediately.
        The bars are counted with a loop keeping track of the streak
            in either horizontal or vertical direction.
        The mxn rectangles are made up of smaller squares,
            e.g. a 3x2 rectangle are two 2x2 stacked vertically.
            Reused part of 1277 solution to shrink all squares by size 1.
            This results in a 2x1 vertical bar. Then reapeat from counting singles and bars.
        Singles are counted in horizontal and vertical bars as well,
            so subtract singles count once from horizontal + vertical.
        """
        NEIGHBORS = [(0, 0), (0, 1), (1, 0), (1, 1)]

        def shrink(mat):
            """Shrink matrix by 1 in horizontal and vertical direction.
            Change matrix in place."""
            m, n = len(mat), len(mat[0])
            for mm in range(m - 1):
                for nn in range(n - 1):
                    for dm, dn in NEIGHBORS:
                        if mat[mm + dm][nn + dn] != 1:
                            mat[mm][nn] = 0
                            break
                    else:
                        mat[mm][nn] = 1
            # return reduced size
            return [row[:-1] for row in mat[:-1]]

        def count_bars(mat, starts, direction, R, C):
            """Counts bars of shape mx1, or 1xn, depending on start and direction.
            Also counts 1x1 rectangles."""
            dr, dc = direction
            ans = 0
            for r, c in starts:
                streak = 0
                while 0 <= r < R and 0 <= c < C:
                    if mat[r][c] == 1:
                        streak += 1
                    else:
                        streak = 0
                    ans += streak
                    r += dr
                    c += dc
            return ans

        ans = 0
        while len(mat) and len(mat[0]):
            R, C = len(mat), len(mat[0])
            count_singles = sum(map(sum, mat))
            count_horizontal_bars = count_bars(
                mat, starts=[(r, 0) for r in range(R)], direction=(0, 1), R=R, C=C
            )
            count_vertical_bars = count_bars(
                mat, starts=[(0, c) for c in range(C)], direction=(1, 0), R=R, C=C
            )
            # singles are also counted in both horizontal and vertical, so subtract once
            add = count_horizontal_bars + count_vertical_bars - count_singles
            ans += add
            if add:
                mat = shrink(mat)
            else:
                break
        return ans


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["numSubmat"],
        data_file="leetcode_1504_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
