import heapq
from typing import List


class Solution:
    def minTimeToReach(self, moveTime: List[List[int]]) -> int:
        """Start from 0,0 and move to n-1,m-1.
        Can only move into room from moveTime. Each room takes 1 second to pass.
        When do we reach bottom right room?"""
        R = len(moveTime)
        C = len(moveTime[0])

        DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]

        visited = set()
        # q = PriorityQueue()
        # q.put((0, (0, 0)))
        # while not q.empty():
        q = [(0, (0, 0))]
        heapq.heapify(q)
        while q:
            # time, (r, c) = q.get()
            time, (r, c) = heapq.heappop(q)
            if (r, c) in visited:
                continue
            visited.add((r, c))
            for dr, dc in DIRECTIONS:
                if (
                    0 <= r + dr < R
                    and 0 <= c + dc < C
                    and (r + dr, c + dc) not in visited
                ):
                    new_time = max(time, moveTime[r + dr][c + dc]) + 1
                    if (r + dr, c + dc) == (R - 1, C - 1):
                        return new_time
                    # q.put((new_time, (r + dr, c + dc)))
                    heapq.heappush(q, (new_time, (r + dr, c + dc)))


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["minTimeToReach"],
        data_file="leetcode_3341_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
