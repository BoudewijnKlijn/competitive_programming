from typing import List


class Solution:
    def spiralMatrixIII(
        self, rows: int, cols: int, rStart: int, cStart: int
    ) -> List[List[int]]:
        DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
        magnitude = 1
        increase_magnitude = True
        pos = (rStart, cStart)
        path = [pos]
        todo = rows * cols - 1
        while todo:
            for dr, dc in DIRECTIONS:
                for _ in range(magnitude):
                    r = pos[0] + dr
                    c = pos[1] + dc
                    pos = (r, c)
                    if 0 <= r < rows and 0 <= c < cols:
                        path.append(pos)
                        todo -= 1
                        if todo <= 0:
                            return path

                increase_magnitude = not increase_magnitude
                if increase_magnitude:
                    magnitude += 1
        return path
