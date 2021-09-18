import sys

from collections import defaultdict, deque


sys.setrecursionlimit(100000)
input = iter(sys.stdin.readlines()).__next__


n, m = map(int, input().split())
a_array = tuple(map(int, input().split()))
edges = list()
for _ in range(n-1):
    edges.append(tuple(map(int, input().split())))

# verbose = 1 if n == 100000 and m == 6 else 0

# print(n, m, a_array[:100], edges[:100], len(a_array), len(edges))
# print('a')
valid = 0

# Make dict with destinations from each vertex.
forward = defaultdict(set)
for edge_start, edge_end in edges:
    forward[edge_start].add(edge_end)
    forward[edge_end].add(edge_start)

# print('b')

# for i, k, v in zip(range(100), forward.keys(), forward.values()):
#     print(i, k, v)

def clean():
    """Remove paths that go in the wrong direction."""
    remove_x_from_y = deque()
    x = 1
    destinations = forward.get(x)
    remove_x_from_y.extend([(x, y) for y in destinations])
    while remove_x_from_y:
        x, y = remove_x_from_y.popleft()
        forward[y].remove(x)
        x = y
        destinations = forward.get(x)
        remove_x_from_y.extend([(x, y) for y in destinations])


    # # print('e')
    # go_to = forward[source]
    # for vertex in go_to:
    #     # print('f')
    #     # print(vertex)
    #     forward[vertex].remove(source)
    #     clean(vertex)

# if verbose: print('c')
clean()
# if verbose: print(' d')

# Make dict with source for each destination (to walk backwards)
backward = {d: {src} for src, destinations in forward.items() for d in destinations}
backward2 = {d: src for src, destinations in forward.items() for d in destinations}

# for i, k, v in zip(range(100), backward2.keys(), backward2.values()):
#     print(i, k, v)


def walk(vertex, src_to_dest, consecutive_cats=0, to_restaurants=True):
    """Walk the paths."""
    global valid

    if a_array[vertex-1] == 1:
        consecutive_cats += 1
        if consecutive_cats > m:
            return
    else:
        consecutive_cats = 0

    go_to = src_to_dest.get(vertex)
    if not go_to:
        valid += 1
    else:
        for destination in go_to:
            walk(destination, src_to_dest, consecutive_cats, to_restaurants)


# # runtime error on 35 (didn't know what it was, but it was an error in clean (too many recursions I think))
# ## and another runtime error after fixing clean.
# walk(1, forward)
# print(valid)

# # too slow on 14
# # walk backward, starting from all the restaurants (they have no destinations)
# for s, d in forward.items():
#     if not d:
#         walk(s, backward, consecutive_cats=0, to_restaurants=False)
# print(valid)


# different solution
# dict with number of consecutive cats at vertex, and maximum along the traveled path so far.
cats = {1: (a_array[1-1], a_array[1-1])}
queue = deque()
queue.extend(forward.get(1))
while queue:
    # print(queue)
    destination = queue.popleft()
    source = backward2.get(destination)
    cat_present_destination = a_array[destination-1]
    consecutive_cats_source, max_consecutive_cats_path = cats.get(source)
    consecutive_cats_destination = consecutive_cats_source + 1 if cat_present_destination else 0
    cats.update({destination: (consecutive_cats_destination,
                               max(max_consecutive_cats_path, consecutive_cats_destination))})
    new_destinations = forward.get(destination, {})
    queue.extend(new_destinations)

valid = 0
for s, d in forward.items():
    if not d and cats.get(s)[1] <= m:
        valid += 1

print(valid)

