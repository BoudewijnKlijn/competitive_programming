from typing import List


class DisjointSet:
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
    def findCircleNum(self, isConnected: List[List[int]]) -> int:
        disjointset = DisjointSet(len(isConnected))
        for i, row in enumerate(isConnected):
            for j, col in enumerate(row[i + 1 :], start=i + 1):
                if col == 1:
                    disjointset.union(i, j)

        unique_roots = set(disjointset.find(x) for x in range(len(isConnected)))
        return len(unique_roots)


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["findCircleNum"],
        data_file="leetcode_0547_data.txt",
    )
