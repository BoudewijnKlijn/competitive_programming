from typing import List


class Solution:
    def secondMinimum(
        self, n: int, edges: List[List[int]], time: int, change: int
    ) -> int:
        """It takes constant time to travel each edge.
        So I just keep track of steps and convert to time later.

        The fastest time would is just the shortest path.
        The 2nd fastest time could be the shortest path + 1 or + 2 nodes.
        +2 nodes if we go to the end, then step back, and then go to the end again.
        +1 node if we can deviate from the shortest path and return to it later with 1 extra node
        or a completely different path which just happens to be 1 node longer.

        We are allowed to go back, but I don't allow it.
        I allow to visit a node again,
        but only if it's at most one step extra compared with the first time.

        Lastly I determine if the 2nd shortest path is +1 or +2 nodes visited."""

        def n_node_visited_to_time(n_nodes_visited, time, change):
            total = 0
            for _ in range(n_nodes_visited):
                if (total // change) % 2 == 1:
                    # red light: set time to next green light
                    total = (total // change + 1) * change
                total += time
            return total

        neighbors = [[] for _ in range(n + 1)]
        for edge in edges:
            neighbors[edge[0]].append(edge[1])
            neighbors[edge[1]].append(edge[0])

        def shortest_path():
            positions = {1}
            steps = 0
            visited_but_okay = dict()
            path_lengths = set()
            while len(path_lengths) < 2:
                new_positions = set()
                for pos in positions:
                    if pos not in visited_but_okay:
                        visited_but_okay[pos] = steps + 1
                    if pos == n:
                        path_lengths.add(steps)
                        continue
                    for neighbor in neighbors[pos]:
                        if neighbor in visited_but_okay and (
                            not visited_but_okay[neighbor] == (steps + 1)
                        ):
                            continue
                        new_positions.add(neighbor)
                positions = new_positions
                steps += 1
                if path_lengths and steps > min(path_lengths) + 2:
                    break
            return path_lengths

        path_lengths = shortest_path()

        second_shortest_path = min(path_lengths) + 2
        if len(path_lengths) > 1:
            second_shortest_path = min(min(path_lengths) + 2, max(path_lengths))
        return n_node_visited_to_time(second_shortest_path, time, change)
