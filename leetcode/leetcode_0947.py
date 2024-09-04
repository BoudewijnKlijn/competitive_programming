from collections import deque
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
    def removeStones(self, stones: List[List[int]]) -> int:
        # return self.create_sets(stones)
        return self.disjoint_sets(stones)

    def disjoint_sets(self, stones: List[List[int]]) -> int:
        # create sets for items in the same row or column
        MAX = 10_001
        rows = [set() for _ in range(MAX)]
        cols = [set() for _ in range(MAX)]
        for i, (x, y) in enumerate(stones):
            rows[x].add(i)
            cols[y].add(i)

        disjointset = DisjointSet(len(stones))
        for set_ in rows + cols:
            if set_:
                a = set_.pop()
                while set_:
                    b = set_.pop()
                    disjointset.union(a, b)
        unique = set(disjointset.find(x) for x in range(len(stones)))
        return len(stones) - len(unique)

    def create_sets(self, stones: List[List[int]]) -> int:
        """With information from editorial that you can always remove all but one cells from a set.
        Answer = number of stones minus number of sets.
        Create sets by joining all neighbors in the rows and columns.
        And repeat for neighbors of neighbors, etc."""
        MAX = 10_001

        # create sets for items in the same row or column
        rows = [set() for _ in range(MAX)]
        cols = [set() for _ in range(MAX)]
        for i, (x, y) in enumerate(stones):
            rows[x].add(i)
            cols[y].add(i)

        unvisited = set(range(len(stones)))
        n_sets = 0
        while unvisited:
            idx = unvisited.pop()
            queue = deque([idx])
            while queue:
                idx = queue.pop()
                x, y = stones[idx]
                for neighbor in rows[x]:
                    if neighbor in unvisited:
                        queue.append(neighbor)
                        unvisited.remove(neighbor)
                for neighbor in cols[y]:
                    if neighbor in unvisited:
                        queue.append(neighbor)
                        unvisited.remove(neighbor)
            n_sets += 1

        return len(stones) - n_sets

    def iteratively_remove(self, stones: List[List[int]]) -> int:
        """Order of removal matters.
        If we remove a stone, we potentially break a link between two other stones.
        Best to remove stones that don't link other stones."""
        MAX = 10_001

        # create sets for items in the same row or column
        rows = [set() for _ in range(MAX)]
        cols = [set() for _ in range(MAX)]
        for i, (x, y) in enumerate(stones):
            rows[x].add(i)
            cols[y].add(i)

        # determine for each stone how many neighbors in row/col/total
        n_neighbors_row = [0 for _ in range(len(stones))]
        n_neighbors_col = [0 for _ in range(len(stones))]
        n_neighbors = [0 for _ in range(len(stones))]
        for i, (x, y) in enumerate(stones):
            n_neighbors_row[i] += len(rows[x]) - 1
            n_neighbors_col[i] += len(cols[y]) - 1
            n_neighbors[i] = n_neighbors_row[i] + n_neighbors_col[i]

        # remove stones iteratively
        ans = 0
        while any(n for n in n_neighbors):
            # remove stones with the least amount of neighbors iteratively
            # it's always safe to remove a stone with zero neighbors in one dimension
            # if that's not possible remove neighbor with least total neighbors
            min_index = self.choose_remove_index(
                n_neighbors_row, n_neighbors_col, n_neighbors
            )

            # remove stone with min neighbors
            x, y = stones[min_index]
            # the stone to be removed shares the row/column with other stones
            # after removing, their n_neighbors is decreased by 1
            # for each stone in the row set, decrease their n_neighbors by 1
            for neighbor_idx in rows[x]:
                n_neighbors[neighbor_idx] -= 1
                n_neighbors_row[neighbor_idx] -= 1
            # for each stone in the col set, decrease their n_neighbors by 1
            for neighbor_idx in cols[y]:
                n_neighbors[neighbor_idx] -= 1
                n_neighbors_col[neighbor_idx] -= 1

            # remove the stone from row/col sets and set neighbors to zero
            rows[x].remove(min_index)
            cols[y].remove(min_index)
            n_neighbors[min_index] = 0
            n_neighbors_row[min_index] = 0
            n_neighbors_col[min_index] = 0

            # increase removed stone count
            ans += 1

        return ans

    def choose_remove_index(self, n_neighbors_row, n_neighbors_col, n_neighbors):
        for i, (nr, nc, n) in enumerate(
            zip(n_neighbors_row, n_neighbors_col, n_neighbors)
        ):
            if n == 0:
                continue
            if nr == 0:
                return i
            if nc == 0:
                return i
        return self.argmin(n_neighbors)

    def argmin(self, array):
        filtered_array = [(i, x) for i, x in enumerate(array) if x > 0]
        return min(filtered_array, key=lambda x: x[1])[0]


if __name__ == "__main__":
    from timing import timing

    timing(
        solution=Solution(),
        funcs=["iteratively_remove", "create_sets", "disjoint_sets"],
        data_file="leetcode_0947_data.txt",
        exclude_data_lines=None,
        check_result=True,
    )
