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


T = int(input())
for t in range(1, T + 1):

    # Gather objects
    K = int(input())
    objects = list()
    for _ in range(K):
        object_coordinates = tuple(map(int, input().split()))
        objects.append(object_coordinates)

    # Brute force for test set 1
    minimum_sum = None
    best = None
    for bottle_coordinates in product(range(-100, 101), range(-100, 101)):
        total_sum = 0
        for object_coordinates in objects:
            total_sum += get_distance(object_coordinates, bottle_coordinates)

        if minimum_sum is None or total_sum < minimum_sum:
            minimum_sum = total_sum
            best = bottle_coordinates

    # print answer
    best_x, best_y = best
    print(f'Case #{t}: {best_x} {best_y}')
