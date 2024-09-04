import heapq
from typing import List


class Solution:
    def maxProbability(
        self,
        n: int,
        edges: List[List[int]],
        succProb: List[float],
        start_node: int,
        end_node: int,
    ) -> float:
        if not edges:
            return 0

        neighbors = {i: dict() for i in range(n)}
        for (a, b), p in zip(edges, succProb):
            neighbors[a].update({b: p})
            neighbors[b].update({a: p})

        edges_visited = set()
        queue = [(-1, start_node)]
        heapq.heapify(queue)
        while queue:
            neg_max_p, pos = heapq.heappop(queue)
            if pos == end_node:
                # early stopping
                return round(-1 * neg_max_p, 5)
            for neighbor, prob in neighbors[pos].items():
                key = tuple(sorted((pos, neighbor)))
                if key in edges_visited:
                    continue

                heapq.heappush(queue, (neg_max_p * prob, neighbor))
                edges_visited.add(key)

        return 0


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["maxProbability"],
        data_file="leetcode_1514_data.txt",
    )
