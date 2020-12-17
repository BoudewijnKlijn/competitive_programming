import timeit
from itertools import product


def load_data():
    with open(input_file, 'r') as f:
        data = f.read().strip().split()
    return data


def parse_data():
    active_cubes = set()
    for x, line in enumerate(data):
        for y, symbol in enumerate(line):
            if symbol == '#':
                active_cubes.add((x, y, 0))
    return active_cubes


def get_neighbours(cube):
    return set(product(
        range(cube[0] - 1, cube[0] + 2),
        range(cube[1] - 1, cube[1] + 2),
        range(cube[2] - 1, cube[2] + 2))) - {cube}


def part1():
    active_cubes = parsed

    # min max x, y, z dimensions
    x_min = 0
    x_max = len(data)
    y_min = 0
    y_max = len(data[0])
    z_min = 0
    z_max = 1

    for cycle in range(6):
        active_next_round = set()
        x_min -= 1
        x_max += 1
        y_min -= 1
        y_max += 1
        z_min -= 1
        z_max += 1
        for cube in product(range(x_min, x_max), range(y_min, y_max), range(z_min, z_max)):
            n_active_around = len(get_neighbours(cube).intersection(active_cubes))
            if cube in active_cubes and n_active_around in [2, 3]:
                active_next_round.add(cube)
            elif cube not in active_cubes and n_active_around == 3:
                active_next_round.add(cube)

        active_cubes = active_next_round

    return len(active_cubes)


def part2():
    pass


def main():
    a1 = part1()
    print(a1)

    a2 = part2()
    print(a2)


if __name__ == '__main__':
    input_file = 'input17.txt'
    data = load_data()
    parsed = parse_data()
    main()

    # t = timeit.Timer('part1(p1=False)', globals=globals())
    # n = 100
    # print(sum(t.repeat(repeat=n, number=1)) / n)
