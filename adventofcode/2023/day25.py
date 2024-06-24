import re
from collections import defaultdict
from queue import Queue

import matplotlib.pyplot as plt
import networkx as nx


def part1(content):
    connections = defaultdict(set)
    for line in content.split("\n"):
        names = re.findall(r"\w+", line)
        first, others = names[0], names[1:]
        for o in others:
            connections[first].add(o)
            connections[o].add(first)

    # visualize_graph(connections)
    # visual inspection shows that if we cut: xqh-ssd, khn-nrs, mqb-qlc it will be disconnected
    connections["xqh"].remove("ssd")
    connections["ssd"].remove("xqh")
    connections["khn"].remove("nrs")
    connections["nrs"].remove("khn")
    connections["mqb"].remove("qlc")
    connections["qlc"].remove("mqb")
    # visualize_graph(connections)  # indeed, two disconnected groups

    # determine group size
    ans = 1
    starts = ["xqh", "ssd"]
    for start in starts:
        queue = Queue()
        queue.put(start)
        visited = set()
        while not queue.empty():
            current = queue.get()
            visited.add(current)
            for neighbor in connections[current]:
                if neighbor not in visited:
                    queue.put(neighbor)
        ans *= len(visited)

    return ans


def visualize_graph(connections):
    """Visualize the puzzle structure with networkx."""
    G = nx.Graph()
    for src, dest in connections.items():
        for d in dest:
            G.add_edge(src, d)

    pos = nx.spring_layout(G)

    nx.draw(G, pos, with_labels=True)
    plt.show()


if __name__ == "__main__":
    """divide the components into two separate, disconnected groups:"""

    SAMPLE = """jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr"""

    # print(part1(SAMPLE))

    with open("day25.txt") as f:
        CONTENT = f.read().strip()

    print(part1(CONTENT))
