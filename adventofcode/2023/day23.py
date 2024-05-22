from collections import defaultdict
from queue import LifoQueue, Queue

import matplotlib.pyplot as plt
import networkx as nx

DIRECTIONS = [
    (-1, 0),  # up
    (0, 1),  # right
    (1, 0),  # down
    (0, -1),  # left
]

FORCED_DIRECTIONS = {
    "^": (-1, 0),
    ">": (0, 1),
    "v": (1, 0),
    "<": (0, -1),
}


def display(history, grid):
    grid = [list(row) for row in grid]
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if (r, c) not in history:
                print(grid[r][c], end="")
            elif (r, c) == history[0]:
                print("S", end="")
            else:
                print("O", end="")
        print()


def part1(content, part2=False):
    """Too slow for part2 (even with fast tracks), but result is correct.
    Can use fast tracks to create a new map."""
    grid = [row for row in content.strip().split("\n")]
    start = (0, 1)
    end = (len(grid) - 1, grid[-1].index("."))

    longest = 0

    # a fast track is a sequence of steps that can be added to history to speed up simulations
    # from the start you have only one way to go (besides going back)
    # from the end you have multiple options to avoid going back the fast track in the wrong way
    fast_tracks = dict()  # start: (end, [every step])
    queue = LifoQueue()
    queue.put((start, [start], [start]))  # (position, history, current_fast_track)
    while not queue.empty():
        position, history, fast_track = queue.get()
        r, c = position
        current_cell = grid[r][c]

        # reached goal
        if position == end and len(history) > longest:
            longest = len(history)

        # apply fast track
        if fast_tracks.get(position):
            new_position, fast_track_ = fast_tracks[position]
            if new_position in history:
                # new position is already visited
                continue
            new_history = history.copy()
            new_history.extend(fast_track_[1:])
            fast_track = [new_position]
            queue.put((new_position, new_history, fast_track))
            continue

        # in part1, some cells have only one direction, in part2 everything is allowed
        directions = DIRECTIONS
        if not part2 and FORCED_DIRECTIONS.get(current_cell):
            directions = [FORCED_DIRECTIONS.get(current_cell)]

        valid_directions = list()
        for dr, dc in directions:
            if (
                r + dr < 0
                or r + dr >= len(grid)
                or c + dc < 0
                or c + dc >= len(grid[0])
            ):
                # new position is out of bounds
                continue
            if grid[r + dr][c + dc] == "#":
                # new position is a tree
                continue
            if len(history) > 2 and history[-2] == (r + dr, c + dc):
                # new position is the previous position
                continue
            valid_directions.append((dr, dc))

        if not valid_directions:
            # dead end
            if len(fast_track) > 2:
                # save fast track
                fast_tracks[fast_track[1]] = (fast_track[-1], fast_track[1:])
            continue

        for dr, dc in valid_directions:
            new_position = (r + dr, c + dc)
            if len(valid_directions) > 1:
                if len(fast_track) > 2:
                    # save fast track
                    fast_tracks[fast_track[1]] = (fast_track[-1], fast_track[1:])
                    if part2:
                        fast_tracks[fast_track[-2]] = (
                            fast_track[0],
                            fast_track[-2::-1],
                        )
                # reset fast track
                fast_track = [position]
            fast_track.append(new_position)

            if new_position in history:
                # new position is already visited
                continue

            # add new position with history to queue
            new_history = history.copy()
            new_history.append(new_position)
            queue.put((new_position, new_history, fast_track))

    return longest - 1


def visualize_graph(node_distances):
    """Visualize the maze/ puzzle structure with networkx."""
    G = nx.Graph()
    for node in node_distances.keys():
        for neighbor, distance in node_distances[node].items():
            G.add_edge(node, neighbor, weight=distance)

    pos = nx.spring_layout(G)
    labels = nx.get_edge_attributes(G, "weight")

    nx.draw(G, pos, with_labels=True)
    plt.show()

    nx.draw(G, pos)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.show()


def get_node_distances(neighbors):
    distances = defaultdict(dict)
    special = [
        (r, c) for r, c in neighbors if len(neighbors[(r, c)]) == 1
    ]  # start and end
    nodes = [(r, c) for r, c in neighbors if len(neighbors[(r, c)]) > 2]
    nodes = nodes + special
    for node in nodes:
        for neighbor in neighbors[node]:
            edge = [node, neighbor]
            enlarge_edge = True
            while enlarge_edge:
                for next_neighbor in neighbors[neighbor]:
                    if next_neighbor in edge:
                        continue
                    else:
                        edge.append(next_neighbor)
                        neighbor = next_neighbor
                        if next_neighbor in nodes:
                            enlarge_edge = False
                            break
            distances[node].update({next_neighbor: len(edge) - 1})
    return distances


def part2(content):
    """Transforming the maze into a graph and using BFS to find the longest path.
    Every cell may only be visited once, which means each node can also only be visited once.
    It is not fast, but it finds the answer in 2-3 minutes."""
    grid = [row for row in content.strip().split("\n")]
    neighbors = get_neighbors(grid)
    start = (0, 1)
    end = (len(grid) - 1, grid[-1].index("."))
    node_distances = get_node_distances(neighbors)

    longest = 0
    queue = Queue()
    queue.put((start, 0, {start}))  # (position, distance, history)
    i = 0
    while not queue.empty():
        i += 1
        position, distance, history = queue.get()
        for next_node, distance_to_next in node_distances[position].items():
            if next_node in history:
                continue
            new_distance = distance + distance_to_next
            new_history = history.copy()
            new_history.add(next_node)
            if next_node == end and new_distance > longest:
                longest = new_distance
                # show progress
                print(i, longest, queue.qsize())  # last output: 30531081 6646 46090
            queue.put((next_node, new_distance, new_history))
    return longest


def get_neighbors(grid):
    neighbors = dict()
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == "#":
                continue
            neighbors[(r, c)] = list()
            for dr, dc in DIRECTIONS:
                if (
                    r + dr < 0
                    or r + dr >= len(grid)
                    or c + dc < 0
                    or c + dc >= len(grid[0])
                ):
                    # new position is out of bounds
                    continue
                if grid[r + dr][c + dc] == "#":
                    # new position is a tree
                    continue
                neighbors[(r, c)].append((r + dr, c + dc))
    return neighbors


if __name__ == "__main__":
    SAMPLE = """#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#"""

    assert part1(SAMPLE, part2=False) == 94

    with open("day23.txt") as f:
        CONTENT = f.read().strip()

    print(part1(CONTENT, part2=False))

    assert part1(SAMPLE, part2=True) == 154
    assert part2(SAMPLE) == 154

    # print(part1(CONTENT, part2=True))  # too slow

    print(part2(CONTENT))  # 6646
