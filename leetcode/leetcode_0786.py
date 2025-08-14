import heapq
from typing import List


class Solution:
    def kthSmallestPrimeFraction(self, arr: List[int], k: int) -> List[int]:
        return self.moving_frontier(arr, k)

    def moving_frontier(self, arr: List[int], k: int) -> List[int]:
        """The smallest number is obviously the fraction with arr[0] and arr[-1].
        Visualize numbers in a matrix, with first row being arr[0]/arr[1:],
            and the next row being arr[1]/arr[2:].
        After the first number, we can either move left in the row, or move down in the column.
        Both 1 step. A large step would always skip a smaller number.
        Add numbers on the moving frontier to a priority queue (heap).
        This is in many cases faster than bruteforce, because not all fractions are calculated,
            but not fast yet."""
        r = 0
        n = len(arr)
        c = n - 1
        fractions = [(arr[r] / arr[c], r, c)]  # val, r, c
        heapq.heapify(fractions)
        added = set()  # to prevent adding the same fraction twice
        i = 0
        while i < k:
            _, r, c = heapq.heappop(fractions)
            # move left
            if c > 0 and (r, c - 1) not in added:
                heapq.heappush(fractions, (arr[r] / arr[c - 1], r, c - 1))
                added.add((r, c - 1))
            # move down
            if r < n - 1 and (r + 1, c) not in added:
                heapq.heappush(fractions, (arr[r + 1] / arr[c], r + 1, c))
                added.add((r + 1, c))
            i += 1
        return [arr[r], arr[c]]

    def bruteforce(self, arr: List[int], k: int) -> List[int]:
        """Calculate all. Then sort. Then give kth element.
        This would be very slow for large arrays."""
        fractions = sorted((a / b, [a, b]) for a in arr for b in arr)
        return fractions[k - 1][1]


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["bruteforce", "moving_frontier"],
        data_file="leetcode_0786_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
