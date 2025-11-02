from collections import deque
from typing import List


class Solution:
    def countUnguarded(
        self, m: int, n: int, guards: List[List[int]], walls: List[List[int]]
    ) -> int:
        return self.start_from_guarded(m, n, guards, walls)

    def start_from_guards(
        self, m: int, n: int, guards: List[List[int]], walls: List[List[int]]
    ) -> int:
        """Start from guards.
        Walk in all 4 directions, inside the grid.
        Stop walking when outside grid, or encountering a wall or guard.
        Cells between guards are checked twice, so could be more efficient.
        Faster than walk_all_cells()
        """
        guards = set(map(tuple, guards))
        walls = set(map(tuple, walls))
        # occupied = guards | walls
        guarded = set()
        DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        for row, col in guards:
            for dr, dc in DIRECTIONS:
                rr, cc = row, col
                while True:
                    rr, cc = rr + dr, cc + dc
                    if (
                        rr < 0
                        or rr >= m
                        or cc < 0
                        or cc >= n
                        or (rr, cc) in guards
                        or (rr, cc) in walls
                    ):
                        # outside grid, or cell is guard or wall
                        break
                    guarded.add((rr, cc))

        return m * n - len(guarded) - len(guards) - len(walls)

    def walk_all_cells(
        self, m: int, n: int, guards: List[List[int]], walls: List[List[int]]
    ) -> int:
        """Use sets to check if guard or wall and to determine unoccupied unguarded cells.
        Walk grid horizontally and vertically.
        Use a queue to collect cells if not sure if guard can see it.
        Add cell and empty queue when completely sure guard sees it.
        We are not sure if not visited a guard yet, or if we visited a wall and then empty cells.
        Slow.
        """
        guards = set(map(tuple, guards))
        walls = set(map(tuple, walls))
        occupied = guards | walls
        guarded = set()
        for row in range(m):
            queue = deque()
            guard = None
            for col in range(n):
                if (row, col) in guards:
                    guard = True
                    # add cells in queue to guarded cells.
                    while queue:
                        guarded.add(queue.popleft())
                elif (row, col) in walls:
                    guard = False
                    # reset queue. useful when not seen a guard yet, or between two walls.
                    queue = deque()
                elif guard is None:
                    # not sure if guard sees it. store cells in queue.
                    queue.append((row, col))
                else:
                    # if no special cells, but have visited guard or wall since start, add to queue
                    # or add to guarded cells.
                    if guard:
                        guarded.add((row, col))
                    elif not guard:
                        queue.append((row, col))

        # same logic, but now walk vertically.
        for col in range(n):
            queue = deque()
            guard = None
            for row in range(m):
                if (row, col) in guards:
                    guard = True
                    while queue:
                        guarded.add(queue.popleft())
                elif (row, col) in walls:
                    guard = False
                    queue = deque()
                elif guard is None:
                    queue.append((row, col))
                else:
                    if guard:
                        guarded.add((row, col))
                    elif not guard:
                        queue.append((row, col))

        return m * n - len(guarded | occupied)


if __name__ == "__main__":
    import os

    from timing import timing

    PROBLEM = "2257"
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
        funcs=["start_from_guards", "walk_all_cells"],
        data_file=data_file,
        exclude_data_lines=None,
        check_result=True,
    )
