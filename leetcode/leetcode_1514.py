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
        ans = 0
        queue = [(-1, None, start_node)]
        heapq.heapify(queue)
        while queue:
            neg_max_p, _, pos = heapq.heappop(queue)
            if pos == end_node:
                ans = min(ans, neg_max_p)
            for neighbor, prob in neighbors[pos].items():
                key = min(pos, neighbor), max(pos, neighbor)
                if key in edges_visited:
                    continue

                heapq.heappush(queue, (neg_max_p * prob, pos, neighbor))
                edges_visited.add(key)

        return round(-1 * ans, 5)


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["maxProbability"],
        data_file="leetcode_1514_data.txt",
        data_lines=None,
    )
