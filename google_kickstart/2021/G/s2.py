import sys
import os
from itertools import product

# Read from stdin.
# input = iter(sys.stdin.readlines()).__next__

# Read from file.
if len(sys.argv) > 1:
    if os.path.exists(sys.argv[1]):
        file_name = sys.argv[1]
        with open(file_name, 'r') as f:
            input = iter(f.readlines()).__next__


def get_distance(object_coordinates, bottle_coordinates):
    min_x, min_y, max_x, max_y = object_coordinates
    x, y = bottle_coordinates
    x_dist = max(0, x - max_x) + max(0, min_x - x)
    y_dist = max(0, y - max_y) + max(0, min_y - y)
    return x_dist + y_dist


def get_coordinate_distance(coordinate, min_coordinate, max_coordinate):
    if coordinate > max_coordinate:
        return max_coordinate - coordinate
    elif coordinate < min_coordinate:
        return min_coordinate - coordinate
    else:
        return 0


def get_distances(x, y):
    x_distances = list()
    y_distances = list()
    for x1, y1, x2, y2 in objects:
        x_dist = get_coordinate_distance(x, x1, x2)
        x_distances.append(x_dist)
        y_dist = get_coordinate_distance(y, y1, y2)
        y_distances.append(y_dist)
    return x_distances, y_distances


def get_median_distance(distances):
    distances = [d for d in distances if d != 0]
    if len(distances) == 0:
        return 0
    elif len(distances) % 2 == 0:
        return sorted(distances)[len(distances) // 2 - 1]
    else:
        return sorted(distances)[len(distances) // 2]


def brute_force(x_range, y_range):
    """Of all possible locations with x in x_range and y in y_range, determine the location with the lowest distance."""
    minimum_distance = None
    best_pos = None
    for (x, y) in product(x_range, y_range):
        total_distance = 0
        for x1, y1, x2, y2 in objects:
            total_distance += abs(get_coordinate_distance(x, x1, x2))
            total_distance += abs(get_coordinate_distance(y, y1, y2))

        if minimum_distance is None or total_distance < minimum_distance:
            minimum_distance = total_distance
            best_pos = (x, y)
    return best_pos, minimum_distance


T = int(input())
for t in range(1, T + 1):

    # Gather objects
    K = int(input())
    objects = list()
    for _ in range(K):
        object_coordinates = tuple(map(int, input().split()))
        objects.append(object_coordinates)

    min_x = min(x for (x, _, _, _) in objects)
    min_y = min(y for (_, y, _, _) in objects)

    # Iterate to find approximate best position.
    alpha = 0.3
    bottle_pos = (min_x, min_y)  # Start at min x and min y
    distance = None
    while True:
        x_distances, y_distances = get_distances(*bottle_pos)
        medians = (get_median_distance(x_distances) * alpha, get_median_distance(y_distances) * alpha)
        new_distance = sum(map(abs, x_distances)) + sum(map(abs, y_distances))
        new_pos = tuple(map(sum, zip(bottle_pos, medians)))
        bottle_pos = new_pos
        if distance is not None and abs(new_distance - distance) < 0.01:
            break
        distance = new_distance

    # Do brute force around approximate position.
    best_pos, minimum_distance = brute_force(range(int(bottle_pos[0]) - 2, int(bottle_pos[0]) + 3),
                                             range(int(bottle_pos[1]) - 2, int(bottle_pos[1]) + 3))

    # Print answer.
    best_x, best_y = best_pos
    print(f'Case #{t}: {best_x} {best_y}')
