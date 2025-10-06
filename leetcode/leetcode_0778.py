import heapq
from collections import deque
from typing import List


class Solution:
    def swimInWater(self, grid: List[List[int]]) -> int:
        return self.dp(grid)

    def with_deque(self, grid: List[List[int]]) -> int:
        """Similar to dp, but tries more paths.
        Slower due to not continuing with best path and therefore tries more paths.

        243ms Beats 5.01% (slowest)
        """
        n = len(grid)
        DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        best = [[None] * n for _ in range(n)]  # minimum water level to get cell

        q = deque([(grid[0][0], (0, 0))])  # max val, last_cell
        ans = n * n
        while q:
            max_val, (r, c) = q.popleft()
            if (r, c) == (n - 1, n - 1):
                if max_val < ans:
                    ans = max_val

            for dr, dc in DIRECTIONS:
                r_new, c_new = r + dr, c + dc
                if r_new < 0 or r_new >= n or c_new < 0 or c_new >= n:
                    # out of bounds
                    continue

                new_max = max(max_val, grid[r_new][c_new])
                if best[r_new][c_new] is None or new_max < best[r_new][c_new]:
                    best[r_new][c_new] = new_max
                    q.append((new_max, (r_new, c_new)))
        return ans

    def dp(self, grid: List[List[int]]) -> int:
        """The water height to get to next cell is max(height of cell, height of path so far).
        The minimum water height to get to a cell is minimum of all possible paths leading to cell.
        There are many possible paths. Even with n<=50.
        Can limit paths by using priority queue (minheap).
            Only continue and remember path if improvement upon current best to reach cell.
            Continue with best cell.

        30ms Beats 55.54% (fastest)
        """
        n = len(grid)
        DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        best = [[None] * n for _ in range(n)]  # minimum water level to get cell

        prio_q = [(grid[0][0], (0, 0))]  # max val, last_cell
        while True:
            max_val, (r, c) = heapq.heappop(prio_q)
            if (r, c) == (n - 1, n - 1):
                return max_val

            for dr, dc in DIRECTIONS:
                r_new, c_new = r + dr, c + dc
                if r_new < 0 or r_new >= n or c_new < 0 or c_new >= n:
                    # out of bounds
                    continue

                new_max = max(max_val, grid[r_new][c_new])
                if best[r_new][c_new] is None or new_max < best[r_new][c_new]:
                    best[r_new][c_new] = new_max
                    heapq.heappush(prio_q, (new_max, (r_new, c_new)))

    def simple(self, grid: List[List[int]]) -> int:
        """Contraints are weak: n x n grid.
        We can find paths that reach the end where the max value encountered may be x.
        Try increasing value of x. Return first value that succeeds.
        Cells have unique values, and shortest route is 2*n - 1 cells long.
            Due to zero index the lowest possible water is 2*n-2.
        Water must at least be as high at the start cell, grid[0][0] and end cell grid[n-1][n-1].

        Works and accepted, but solution can be more efficient.
        55ms Beats 20.41%
        """
        n = len(grid)
        DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        def bfs(max_val):
            seen = set()
            q = deque([(0, 0)])
            while q:
                r, c = q.popleft()
                if (r, c) == (n - 1, n - 1):
                    return True
                if (r, c) in seen:
                    continue
                seen.add((r, c))
                for dr, dc in DIRECTIONS:
                    r2, c2 = r + dr, c + dc
                    if (r2, c2) in seen or r2 < 0 or r2 >= n or c2 < 0 or c2 >= n:
                        continue
                    if grid[r2][c2] <= max_val:
                        q.append((r2, c2))
            return False

        start = max(2 * n - 2, grid[0][0], grid[n - 1][n - 1])
        for max_val in range(start, n * n + 1):
            if bfs(max_val):
                return max_val


if __name__ == "__main__":
    import os

    from timing import timing

    PROBLEM = "0778"
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
        funcs=["simple", "dp", "with_deque"],
        data_file=data_file,
        exclude_data_lines=None,
        check_result=True,
    )
