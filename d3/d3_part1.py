import time
import re
import numpy as np


def read_file(filename):
    with open(filename, 'r') as f:
        return f.read()


def get_details(line_item):
    details = [int(i) for i in re.findall(r"[\d]+", line_item)]
    if len(details) == 5:
        return details
    else:
        return [0]*5


def get_max_dimensions(contents):
    max_x, max_y = 0, 0
    for line_item in contents.split('\n'):
        _, x, y, width, height = get_details(line_item)

        if x + width > max_x:
            max_x = x + width
        if y + height > max_y:
            max_y = y + height

    return max_x, max_y


def fill_fabric(fabric, contents):
    for line_item in contents.split('\n'):
        _, x, y, width, height = get_details(line_item)
        fabric[x:x+width, y:y+height] += 1

    return fabric


def main():
    contents = read_file('input.txt')
    width, height = get_max_dimensions(contents)
    print(f"Dimensions of fabric: {width}, {height}")

    fabric = np.zeros((width, height), dtype=int)
    fabric = fill_fabric(fabric, contents)

    answer = sum(sum(fabric >= 2))
    print(f"Answer: {answer}")


if __name__ == "__main__":
    start_time = time.time()
    main()
    execution_time = time.time() - start_time
    print("Execution time: {:.5f}s".format(execution_time))
