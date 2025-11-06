from collections import defaultdict, deque
from typing import List


class DisjointSet:
    """Copied from 0547."""

    def __init__(self, size):
        self.root = list(range(size))
        self.rank = [1] * size

    def find(self, node):
        """Find root of node.
        Optimized with path compression"""
        root = self.root[node]
        if root == node:
            return root
        self.root[node] = self.find(root)
        return self.root[node]

    def union(self, a, b):
        """Combine.
        Optimized with union by rank"""
        roota = self.find(a)
        rootb = self.find(b)
        if roota != rootb:
            if self.rank[a] > self.rank[b]:
                self.root[rootb] = roota
            elif self.rank[b] > self.rank[a]:
                self.root[roota] = rootb
            else:
                self.root[rootb] = roota
                self.rank[a] += 1


class Solution:
    def processQueries(
        self, c: int, connections: List[List[int]], queries: List[List[int]]
    ) -> List[int]:
        """Create power grids (connected stations).
        Create deques for each power grid with sorted stations (small to large).
        Iterate over queries. Keep deques up to date with smallest station that is ON at
            first index. If empty deque return -1.
        """
        # Create power grids (connected stations)
        groups = DisjointSet(size=c + 1)
        for u, v in connections:
            groups.union(u, v)

        # Create deques for each power grid with sorted stations (small to large).
        sorted_groups = defaultdict(deque)
        for station in range(1, c + 1):
            root = groups.find(station)
            sorted_groups[root].append(station)

        ans = list()
        off = set()
        for type_, station in queries:
            root = groups.find(station)
            if type_ == 1:
                if station not in off:
                    # Station itself is on.
                    ans.append(station)
                elif sorted_groups[root]:
                    # First position contains smallest station that is ON.
                    ans.append(sorted_groups[root][0])
                else:
                    # All stations in grid are off.
                    ans.append(-1)
            else:
                off.add(station)
                # Keep deque up to date with smallest station that is ON at first index.
                while sorted_groups[root] and sorted_groups[root][0] in off:
                    sorted_groups[root].popleft()
        return ans


if __name__ == "__main__":
    import os

    from timing import timing

    PROBLEM = "3607"
    data_file = os.path.join(os.path.dirname(__file__), f"leetcode_{PROBLEM}_data.txt")

    # # generate testcases
    # import sys

    # sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    # from generic.helper import InputInteger, InputList, generate_testcases

    # arr1 = InputList(n_min_max=(2, 100_000), val_min_max=(0, 10_000))
    # int1 = InputInteger(val_min_max=(0, 10_000))
    # vars = generate_testcases(structure=(arr1,), n=1, data_file=data_file, solver=None)

    timing(
        solution=Solution(),
        funcs=["processQueries"],
        data_file=data_file,
        exclude_data_lines=None,
        check_result=True,
    )
