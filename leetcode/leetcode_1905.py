from collections import deque
from typing import List


class Solution:
    def countSubIslands(self, grid1: List[List[int]], grid2: List[List[int]]) -> int:
        """Find islands in grid2.
        For each island check if all cells are land in grid1.
        Not needed to check for islands in grid1.
        If all cells are land, then they are part of the same island.
        """
        islands2 = self.get_islands(grid2)
        ans = 0
        for island2 in islands2:
            if all(grid1[r][c] == 1 for r, c in island2):
                ans += 1
        return ans

    def get_islands(self, grid):
        unvisited_land_cells = set()
        for r, row in enumerate(grid):
            for c, cell in enumerate(row):
                if cell == 1:
                    unvisited_land_cells.add((r, c))

        DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        islands = list()
        while unvisited_land_cells:
            island = set()
            start = unvisited_land_cells.pop()
            queue = deque([start])
            while queue:
                r, c = queue.pop()
                island.add((r, c))
                for dr, dc in DIRECTIONS:
                    if (r + dr, c + dc) in unvisited_land_cells:
                        queue.append((r + dr, c + dc))
                        unvisited_land_cells.remove((r + dr, c + dc))
            islands.append(island)
        return islands

    def naive(self, grid1: List[List[int]], grid2: List[List[int]]) -> int:
        """get islands in grid1
        get islands in grid2
        for each island in grid2, check if subset of island in grid1
        works, but time limit exceeded, 54/57 passed
        """
        islands1 = self.get_islands(grid1)
        islands2 = self.get_islands(grid2)
        ans = 0
        for island2 in islands2:
            for island1 in islands1:
                if island2.issubset(island1):
                    ans += 1
                    break
        return ans


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["countSubIslands"],
        data_file="leetcode_1905_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
