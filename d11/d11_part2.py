import time
import numpy as np


def calc_power_level(x, y, serial_number):
    rack_id = x + 10
    power_level_start = rack_id * y
    power_level = power_level_start + serial_number
    power_level = power_level * rack_id
    try:
        power_level = int(str(power_level)[-3])
    except:
        power_level = 0
    power_level -= 5

    return power_level


def main():
    """
    Not an elegant solution. Just brute force, and you can manually stop the iteration once you see it doesn't change
    anymore.
    """

    serial_number = 7315
    x_min, x_max, y_min, y_max = 1, 300, 1, 300

    assert calc_power_level(122, 79, 57) == -5
    assert calc_power_level(217, 196, 39) == 0
    assert calc_power_level(101, 153, 71) == 4

    grid = np.zeros((x_max+1, y_max+1))
    for x in range(x_min, x_max + 1):
        for y in range(y_min, y_max + 1):
            grid[x, y] = calc_power_level(x, y, serial_number)

    max_level = 0
    for size in range(1, 300 + 1):
        print(size)
        for x in range(x_min, x_max + 1 - (size-1)):
            for y in range(y_min, y_max + 1 - (size-1)):
                level = sum(sum(grid[x:x+size, y:y+size]))
                if level > max_level:
                    max_level = level
                    top_left = (x, y, size)
                    print(top_left)

    answer = top_left
    print(f"Answer: {answer}")


if __name__ == "__main__":
    start_time = time.time()
    main()
    execution_time = time.time() - start_time
    print("Execution time: {:.5f}s".format(execution_time))
