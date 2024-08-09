from itertools import product
from typing import List


class Solution:
    def numMagicSquaresInside(self, grid: List[List[int]]) -> int:
        R = len(grid)
        C = len(grid[0])

        def is_magic(r, c):
            # create flat list
            numbers = []
            for rr in range(r, r + 3):
                for cc in range(c, c + 3):
                    numbers.append(grid[rr][cc])

            # check occurence 1 to 9
            if sorted(numbers) != list(range(1, 10)):
                return False

            # check horizontal
            if sum((numbers[:3])) != sum((numbers[3:6])) != sum((numbers[6:])):
                return False

            # check vertical
            if (
                sum((numbers[0], numbers[3], numbers[6]))
                != sum((numbers[1], numbers[4], numbers[7]))
                != sum((numbers[2], numbers[5], numbers[8]))
            ):
                return False

            # check diagonal
            if (
                sum((numbers[:3]))
                != sum((numbers[0], numbers[4], numbers[8]))
                != sum((numbers[2], numbers[4], numbers[6]))
            ):
                return False

            return True

        ans = 0
        for topleft in product(range(R - 2), range(C - 2)):
            if is_magic(*topleft):
                ans += 1
        return ans
