from typing import List


class Solution:
    def maxPoints(self, points: List[List[int]]) -> int:
        return self.adjust_row_values(points)

    def adjust_row_values(self, points: List[List[int]]) -> int:
        """Adjust row values before the double inner loop.
        Say we have a 3 rows: [4,0,4], then [1,5,1] and then [4,0,0].
        We can adjust the values to reflect the switching columns.
        Rows becomes, [4, 3, 4] then [4,5,4] and [4,3,2].
        Then the sum per column and then the max.
        Wrong answer: thinking error."""
        R = len(points)
        C = len(points[0])
        adjusted_rows = []
        for r in range(R):
            # initialization to use the same loop for all columns
            prev_col_max = points[r][0] + 1
            adjusted_column = []
            for c in range(C):
                prev_col_max = max(
                    prev_col_max - 1, *(val - i for i, val in enumerate(points[r][c:]))
                )
                adjusted_column.append(prev_col_max)
            adjusted_rows.append(adjusted_column)
            # TODO: make faster with pointers moving out from the max. faster than two nested loops.

        return max(map(sum, zip(*adjusted_rows)))

    def faster2(self, points: List[List[int]]) -> int:
        """Time limit exceeded.
        141/157 passed."""
        best = points[0]
        for row_next in points[1:]:
            best = [
                extra_points
                + max(
                    current_points - abs(col_next - col_current)
                    for col_current, current_points in enumerate(best)
                )
                for col_next, extra_points in enumerate(row_next)
            ]
        return max(best)

    def faster(self, points: List[List[int]]) -> int:
        """Time limit exceeded.
        141/157 passed."""
        R = len(points)  # M
        C = len(points[0])  # N

        best = points[0]
        for r, row_next in enumerate(points[1:], start=1):
            best_next = [0] * C
            for c_next, extra_points in enumerate(row_next):
                best_next[c_next] = extra_points + max(
                    current_points - abs(c_next - c_current)
                    for c_current, current_points in enumerate(best)
                )
            best = best_next
        return max(best)

    def simple(self, points: List[List[int]]) -> int:
        """Time limit exceeded.
        140/157 passed."""
        # too many columns to try every route: C ** R and 1 <= m, n <= 1e5
        # every row I can determine the maximum number of points per cell
        # from there I go to the next cell and again determine maximum
        R = len(points)  # M
        C = len(points[0])  # N

        best = points[0]
        for r, row_next in enumerate(points[1:], start=1):
            best_next = [0] * C
            for c_next, extra_points in enumerate(row_next):
                for c_current, current_points in enumerate(best):
                    best_next[c_next] = max(
                        best_next[c_next],
                        current_points + extra_points - abs(c_next - c_current),
                    )
            best = best_next
        return max(best)


if __name__ == "__main__":
    from timing import timing

    timing(
        data_file="leetcode_1937_data.txt",
        funcs=[
            # "simple",
            # "faster",
            "faster2",
            "adjust_row_values",
        ],
        args_idx=[0, 1, 2, 4],  # 4:108657
        solution=Solution(),
    )
