from queue import PriorityQueue


class Solution:
    def findTheCity(
        self, n: int, edges: List[List[int]], distanceThreshold: int
    ) -> int:
        neighbors = [list() for _ in range(n)]
        for b, e, w in edges:
            neighbors[b].append((e, w))
            neighbors[e].append((b, w))

        def get_nodes_in_reach(start):
            q = PriorityQueue()
            q.put((0, start, set()))
            reachable = set()
            while not q.empty():
                sum_weight, pos, visited = q.get()
                if pos in reachable:
                    # already know this is reachable, but via a shorter path
                    # since we are using priorityqueue sorted on sum_weight
                    continue
                visited.add(pos)
                reachable.add(pos)
                for neighbor, weight in neighbors[pos]:
                    if neighbor in visited:
                        continue
                    if (new := sum_weight + weight) <= distanceThreshold:
                        q.put((new, neighbor, visited))
            return len(reachable) - 1

        cities = list(reversed(range(n)))
        return min(cities, key=get_nodes_in_reach)
