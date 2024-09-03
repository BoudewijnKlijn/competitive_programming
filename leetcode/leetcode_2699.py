from collections import deque
from pprint import pprint
from typing import List


class Solution:
    def modifiedGraphEdges(
        self, n: int, edges: List[List[int]], source: int, destination: int, target: int
    ) -> List[List[int]]:
        """Many answers possible so I have to make my own function to check answer.
        First step is to determine paths, and store weights along the way.
        Then adjust weights to make a path that is equal to target. If possible"""
        # generate neighbor dict
        neighbors = {i: [] for i in range(n)}
        weights = dict()
        for a, b, w in edges:
            weights[(a, b)] = w
            weights[(b, a)] = w
            neighbors[a].append(b)
            neighbors[b].append(a)
        # print(neighbors)
        # print(weights)

        # weights should be 1 at least
        adjusted_weights = {k: max(v, 1) for k, v in weights.items()}
        # print(adjusted_weights)

        # get paths
        paths = list()
        queue = deque()
        queue.append([source])
        while queue:
            path = queue.popleft()
            pos = path[-1]
            if pos == destination:
                paths.append(path)
                continue
            for neighbor_pos in neighbors[pos]:
                if neighbor_pos not in path:
                    queue.append(path + [neighbor_pos])

        # analyse paths
        path_info = dict()
        for i, path in enumerate(paths):
            total_weight = 0
            min_total_weight = 0
            minus_1_weights = 0
            unadjustable_weight = 0
            for a, b in zip(path, path[1:]):
                weight = weights[(a, b)]
                if weight == -1:
                    minus_1_weights += 1
                else:
                    unadjustable_weight += weight
                total_weight += weight
                min_total_weight += adjusted_weights[(a, b)]
            path_info[i] = {
                "path": path,
                "nodes": len(path),
                "edges": len(path) - 1,
                "minus_1_weights": minus_1_weights,
                "unadjustable_weight": unadjustable_weight,
                "total_weight": total_weight,
                "min_total_weight": min_total_weight,
            }
        pprint(path_info, sort_dicts=False)

        # if unadjustable weight is lower than target and no minus 1 weights, its impossible
        for info in path_info.values():
            if info["unadjustable_weight"] < target and info["minus_1_weights"] == 0:
                return []

        # adjust weights (edges)
        # such that one (or more) paths become the shortest and have length == target
        pass  ## TODO

        # verify answer
        self.verify_answer(edges, source, destination, target)

    def verify_answer(self, edges, source, destination, target):
        # weights have to be integers and larger than 0
        assert all(isinstance(weight, int) for *_, weight in edges)
        # assert all(weight > 0 for *_, weight in edges)

        pass


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["modifiedGraphEdges"],
        data_file="leetcode_2699_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
