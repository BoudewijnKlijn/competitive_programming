import heapq
from typing import List


class Solution:
    def maxPoints(self, points: List[List[int]]) -> int:
        return self.lookback(points)

    def maximum_points_row_sweep_twice(self, col_points: List[int]) -> List[int]:
        """Helper function
        (Faster than the heap version. Sweep twice: once left to right and once right to left.)
        In some row, each column gives a certain number of points.
        This function returns the maximum number of points per column.
        Columns with few points, but close to a column with many points still give many points.
        Each column away subtracts 1.
        Examples:
            [4, 0, 4] -> [4, 3, 4]
            [1, 5, 1] -> [4, 5, 4]
            [4, 0, 0] -> [4, 3, 2]"""
        best = [0] * len(col_points)
        best[0] = col_points[0]
        # move left to right
        for i in range(1, len(col_points)):
            best[i] = max(best[i - 1] - 1, col_points[i])
        # move right to left
        for i in range(len(col_points) - 2, -1, -1):
            best[i] = max(best[i + 1] - 1, best[i])
        return best

    def maximum_points_row(self, col_points: List[int]) -> List[int]:
        """Helper function.
        In some row, each column gives a certain number of points.
        This function returns the maximum number of points per column.
        Columns with few points, but close to a column with many points still give many points.
        Each column away subtracts 1.
        Examples:
            [4, 0, 4] -> [4, 3, 4]
            [1, 5, 1] -> [4, 5, 4]
            [4, 0, 0] -> [4, 3, 2]"""
        C = len(col_points)
        best = [0] * C
        q = sorted((-value, c) for c, value in enumerate(col_points))
        heapq.heapify(q)
        visited = set()
        while q:
            neg_val, pos = heapq.heappop(q)
            visited.add((neg_val, pos))
            if neg_val < best[pos]:
                best[pos] = neg_val
                if pos > 0:
                    if (neg_val + 1, pos - 1) not in visited:
                        heapq.heappush(q, (neg_val + 1, pos - 1))
                        visited.add((neg_val + 1, pos - 1))
                if pos < C - 1:
                    if (neg_val + 1, pos + 1) not in visited:
                        heapq.heappush(q, (neg_val + 1, pos + 1))
                        visited.add((neg_val + 1, pos + 1))
        return [-val for val in best]

    def lookback(self, points: List[List[int]]) -> int:
        """Look back at the previous row.
        Then determine the maximum number of points to get from that row for each column.
        Then add the points of the current row and store result for the next iteration, or to return.
        """
        prev = points[0]
        for row_points in points[1:]:
            # best_prev = self.maximum_points_row(prev)
            best_prev = self.maximum_points_row_sweep_twice(prev)
            prev = list(map(sum, zip(row_points, best_prev)))
        return max(prev)

    def adjust_row_values(self, points: List[List[int]]) -> int:
        """Adjust row values before the double inner loop.
        Say we have a 3 rows: [4,0,4], then [1,5,1] and then [4,0,0].
        We can adjust the values to reflect the switching columns.
        Rows becomes, [4, 3, 4] then [4,5,4] and [4,3,2].
        Then the sum per column and then the max.
        Wrong answer: thinking error."""
        R = len(points)
        C = len(points[0])
        adjusted_rows = [points[0]]
        for r in range(1, R):
            adjusted_column = []
            # penalty should be two, because forth and back. except for the last row
            penalty = 1 if r == R - 1 else 2
            # initialization to use the same loop for all columns
            prev_col_max = points[r][0] + penalty
            for c in range(C):
                prev_col_max = max(
                    prev_col_max - penalty,
                    *(val - i * penalty for i, val in enumerate(points[r][c:]))
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
        solution=Solution(),
        funcs=[
            # "simple",
            # "faster",
            # "faster2",
            # "adjust_row_values",
            "lookback",
        ],
        data_file="leetcode_1937_data.txt",
        # data_lines=[0, 1, 2, 3, 4, 5],
    )
