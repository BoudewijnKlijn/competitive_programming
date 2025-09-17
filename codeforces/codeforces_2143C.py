import heapq
import math
import os
from collections import Counter, defaultdict, deque


def solve():
    """We are given a tree with n nodes (vertices) and n-1 edges.
    We must assign values to each node: a permutation, so each a different value from 1 to n.
    The values we assign determines which values the edges get.
    The goal is to maximize the edge values.
    The edge value is determined based on the permutation value of the two nodes.
    In this example:
    1 2 2 1
    2 3 3 2
    Nodes 1 and 2 are connected. If node 1 has a higher permutation value, the edge has value 2, otherwise 1.
    Nodes 2 and 3 are connected. If node 2 has a higher permutation value, the edge has value 3, otherwise 2.

    The edge always has a value, so I could subtract the minimum, such that min becomes zero
        and other becomes value-min.
    Then I can determine the total gain left over per node.
    Order the nodes by total gain, and assign permutation values high to low.

    Seems incorrect...WIP
    """
    n = int(input())
    total_gain_nodes = {i: 0 for i in range(1, n + 1)}
    edges = list()
    ans = 0
    for _ in range(n - 1):
        u, v, x, y = tuple(map(int, input().split()))
        # total_gain_nodes[u] += x
        # total_gain_nodes[v] += y
        if x < y:
            total_gain_nodes[v] += y - x
            ans += x
        else:
            total_gain_nodes[u] += x - y
            ans += y
        edges.append((u, v, x, y))
    print(edges)
    print(total_gain_nodes)
    print(ans)


if __name__ == "__main__":
    MULTIPLE_TESTS = True

    if not os.path.exists(os.path.join("codeforces", "LOCAL")):
        t = 1
        if MULTIPLE_TESTS:
            t = int(input())

        for _ in range(t):
            solve()
    else:
        import test_runner

        test_runner.main(solve, __file__, MULTIPLE_TESTS)
