import timeit
from itertools import product
from collections import defaultdict


def load_data():
    with open(input_file, 'r') as f:
        data = f.read().strip().split()
    return data


def parse_data():
    pass


action_mapping = {
    # action: (dx, dy)
    'N': (0, 1),
    'E': (1, 0),
    'S': (0, -1),
    'W': (-1, 0),
}
directions = 'NESW'


def part1():
    x, y = 0, 0
    facing_direction = 'E'
    for instruction in data:
        action, value = instruction[0], int(instruction[1:])
        if action in 'NESW':
            dx, dy = action_mapping[action]
            x, y = x + value * dx, y + value * dy
        elif action in 'LR':
            turns_of_90 = value // 90
            direction_index = directions.index(facing_direction)
            new_direction_index = (direction_index - turns_of_90) % 4 if action == 'L' else \
                                  (direction_index + turns_of_90) % 4
            facing_direction = directions[new_direction_index]
        elif action == 'F':
            dx, dy = action_mapping[facing_direction]
            x, y = x + value * dx, y + value * dy
        else:
            ValueError()

    return abs(x) + abs(y)


def part2():
    pass


def main():
    a1 = part1()
    print(a1)

    a2 = part2()
    print(a2)


if __name__ == '__main__':
    input_file = 'input12.txt'
    data = load_data()
    parsed = parse_data()
    main()

    # t = timeit.Timer('part1(p1=False)', globals=globals())
    # n = 100
    # print(sum(t.repeat(repeat=n, number=1)) / n)
