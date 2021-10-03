import re
import time


def read_file(filename):
    with open(filename, 'r') as f:
        return f.read().split('\n')


def get_boundaries(contents, offset=0):
    min_x, max_x, min_y, max_y = None, None, None, None
    for x, y in contents:
        if min_x is None or x < min_x:
            min_x = x
        elif max_x is None or x > max_x:
            max_x = x

        if min_y is None or y < min_y:
            min_y = y
        elif max_y is None or y > max_y:
            max_y = y

    return min_x - offset, max_x + offset, min_y - offset, max_y + offset


def get_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


def get_size_safe_region(centers):
    areas = {i: {'center_x': x, 'center_y': y, 'size': 0} for i, (x, y) in enumerate(centers)}

    min_x, max_x, min_y, max_y = get_boundaries(centers)
    width = max_x - min_x + 1
    height = max_y - min_y + 1

    safe_region_size = 0
    total_distance_threshold = 10000
    for row in range(width):
        x = row + min_x
        for col in range(height):
            y = col + min_y

            total_distance = 0
            for center in areas:
                distance = get_distance(x, y, areas[center]['center_x'], areas[center]['center_y'])
                total_distance += distance

            if total_distance < total_distance_threshold:
                safe_region_size += 1

    return safe_region_size


def main():
    contents = read_file('input.txt')
    centers = [tuple([int(i) for i in re.findall('[\d]+', c)]) for c in contents if c]

    answer = get_size_safe_region(centers)
    print(f"Answer: {answer}")


if __name__ == "__main__":
    start_time = time.time()
    main()
    execution_time = time.time() - start_time
    print("Execution time: {:.5f}s".format(execution_time))
