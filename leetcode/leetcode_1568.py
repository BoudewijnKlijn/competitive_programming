from collections import deque
from typing import List


class Solution:
    def minDays(self, grid: List[List[int]]) -> int:
        # we need to break connections such that there are 2 or more islands
        # first i need to find the number of islands
        # if there is more than 1 island, return 0
        # if there is only 1 island, i need to break it up
        # find all island cells and figure out to how many cells they are connected
        # if one of them is only connected via 1 cell, return 1

        m = len(grid)
        n = len(grid[0])

        DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        # get island cells
        island_cells = set()
        for r in range(m):
            for c in range(n):
                if grid[r][c] == 1:
                    island_cells.add((r, c))

        n_island_cells = len(island_cells)
        match n_island_cells:
            case 0:
                return 0
            case 1:
                return 1
            # with 2 island cells, ans could be 0 or 2

        # get neighboring island cells for each island cell
        island_cell_neighbors = dict()
        for r, c in island_cells:
            island_cell_neighbors[(r, c)] = [
                (r + dr, c + dc)
                for dr, dc in DIRECTIONS
                if (r + dr, c + dc) in island_cells
            ]

        # make connected island
        def get_n_islands(island_cells, remove=None):
            n_islands = 0
            visited = set()
            if remove is not None:
                visited.add(remove)

            for r, c in island_cells:
                if (r, c) not in visited:
                    q = deque()
                    q.append((r, c))
                    while q:
                        r, c = q.pop()
                        visited.add((r, c))
                        for nr, nc in island_cell_neighbors[(r, c)]:
                            if (nr, nc) not in visited:
                                q.append((nr, nc))
                                visited.add((r, c))
                    n_islands += 1
                    if n_islands > 1:
                        # stop iterating if we have more than 1 island
                        return n_islands
            return n_islands

        n_islands = get_n_islands(island_cells)

        if n_islands > 1:
            return 0
        # with 1 island and 2 cells, ans has to be 2
        if n_island_cells == 2:
            return 2

        # if one island cell has only 1 neighbor, we can remove that to create 2 island, so return 1
        min_neighbors = None
        for (r, c), neighbors in island_cell_neighbors.items():
            if min_neighbors is None or len(neighbors) < min_neighbors:
                min_neighbors = len(neighbors)
                if min_neighbors == 1:
                    return 1

        # check if we can create 2 islands by removing 1 cell
        for remove_cell in island_cells:
            tmp_n_islands = get_n_islands(island_cells, remove=remove_cell)
            if tmp_n_islands > 1:
                return 1

        # so 1 island.
        match n_island_cells:
            case 3:
                return 1
            case 4:  # these must have more than 1 neighbor, which means square
                return 2
            case _:
                return min_neighbors


# s = Solution()
# g = [
#     [1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
#     [1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1],
#     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#     [1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
# ]
# print(s.minDays(g))  # 2

# g = [[0, 1, 1], [1, 1, 1], [1, 1, 0]]
# print(s.minDays(g))  # 1
