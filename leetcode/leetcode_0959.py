from itertools import product
from queue import Queue
from typing import List


class Solution:
    def regionsBySlashes(self, grid: List[str]) -> int:
        # besides the tile coordinates, every tile has 4 sides, which we also track
        # left, top, right, bottom = 0, 1, 2, 3
        # we start at the top left corner on the left side, which is 0, 0, 0
        # then we determine all sides which are connected
        # then we determine neighbors of the sides
        # repeat from there
        # when queue empty, region is complete. start from another unvisited tile

        def create_region(start):
            region = set()
            queue = Queue()
            queue.put(start)
            while not queue.empty():
                r, c, side = queue.get()
                if (r, c, side) in region:
                    continue
                region.add((r, c, side))
                symbol = grid[r][c]

                # find connected sides
                match symbol:
                    case " ":
                        connected_sides = set(range(4))
                    case "/":
                        if side in [0, 1]:
                            connected_sides = {0, 1}
                        elif side in [2, 3]:
                            connected_sides = {2, 3}
                    case "\\":
                        if side in [0, 3]:
                            connected_sides = {0, 3}
                        elif side in [1, 2]:
                            connected_sides = {1, 2}

                # find neighbors of sides
                for connected_side in connected_sides:
                    region.add((r, c, connected_side))
                    match connected_side:
                        case 0:
                            # tile to left: right side
                            neighbor = (r, c - 1, 2)
                        case 1:
                            # tile above: bottom side
                            neighbor = (r - 1, c, 3)
                        case 2:
                            # tile to right: left side
                            neighbor = (r, c + 1, 0)
                        case 3:
                            # tile below: top side
                            neighbor = (r + 1, c, 1)

                    # add neighbor to region and queue
                    if neighbor in region:
                        continue
                    if 0 <= neighbor[0] < n and 0 <= neighbor[1] < n:
                        # has to be within the grid
                        queue.put(neighbor)
            return region

        n = len(grid)
        all_options = product(range(n), range(n), range(4))

        visited = set()
        ans = 0
        for start in all_options:
            if start in visited:
                continue
            ans += 1
            region = create_region(start)
            visited.update(region)
        return ans
