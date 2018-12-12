import time
import re
import numpy as np
import matplotlib.pyplot as plt


def read_file(filename):
    with open(filename, 'r') as f:
        return f.read().split('\n')


def parse(contents):
    parsed = []
    for line in contents:
        ints = [int(i) for i in re.findall(r'[-\d]+', line)]
        parsed.append(ints)
    return parsed


def evolve(contents, seconds=1):
    for _ in range(seconds):
        for i, (x, y, dx, dy) in enumerate(contents):
            new_x = x + dx
            new_y = y + dy
            contents[i] = [new_x, new_y, dx, dy]
    return contents


def calc_variance(contents, column):
    data = np.array(contents).reshape(-1, 4)
    return data[:, column].var()


def main():
    """
    If the light are to make a text, they will probably be one a line; more or less the same x coordinate, means little
    variance.
    """
    contents = read_file('input.txt')[:-1]
    parsed = parse(contents)

    max_runs = 15000
    y_variances = []
    for _ in range(max_runs):
        parsed = evolve(parsed, 1)
        y_variances.append(calc_variance(parsed, 1))

    # plt.plot(y_variances)
    # plt.show()

    np_y_variances = np.array(y_variances)
    minimum = np_y_variances.argmin()

    parsed = parse(contents)
    parsed_minimum = evolve(parsed, minimum + 1)
    x = [coordinates[0] for coordinates in parsed_minimum]
    y = [coordinates[1] * -1 for coordinates in parsed_minimum]
    plt.scatter(x, y)
    plt.show()

    answer = 'kzhgrjgz'
    print(f"Answer part 1: {answer}")
    print(f"Answer part 2: {minimum + 1}")


if __name__ == "__main__":
    start_time = time.time()
    main()
    execution_time = time.time() - start_time
    print("Execution time: {:.5f}s".format(execution_time))
