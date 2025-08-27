from itertools import product
from functools import reduce


def load_data():
    with open(input_file, 'r') as f:
        data = f.read().strip().split()
    return data


def parse_data():
    active_cubes = set()
    active_hypercubes = set()
    for x, line in enumerate(data):
        for y, symbol in enumerate(line):
            if symbol == '#':
                active_cubes.add((x, y, 0))
                active_hypercubes.add((x, y, 0, 0))
    return active_cubes, active_hypercubes


def get_neighbours(cube):
    return set(product(
        range(cube[0] - 1, cube[0] + 2),
        range(cube[1] - 1, cube[1] + 2),
        range(cube[2] - 1, cube[2] + 2))) - {cube}


def get_neighbours_hyper(cube):
    return set(product(
        range(cube[0] - 1, cube[0] + 2),
        range(cube[1] - 1, cube[1] + 2),
        range(cube[2] - 1, cube[2] + 2),
        range(cube[3] - 1, cube[3] + 2))) - {cube}


def part1():
    active_cubes, _ = parsed

    for cycle in range(6):
        active_next_round = set()
        neighbours_active_cells = reduce(lambda x, y: x.union(y),
                                         [get_neighbours(active_cube) for active_cube in active_cubes])
        for cube in neighbours_active_cells:
            n_active_around = len(get_neighbours(cube).intersection(active_cubes))
            if cube in active_cubes and n_active_around in [2, 3]:
                active_next_round.add(cube)
            elif cube not in active_cubes and n_active_around == 3:
                active_next_round.add(cube)

        active_cubes = active_next_round

    return len(active_cubes)


def part2():
    _, active_hypercubes = parsed

    for cycle in range(6):
        active_next_round = set()
        neighbours_active_cells = reduce(lambda x, y: x.union(y),
                                         [get_neighbours_hyper(active_cube) for active_cube in active_hypercubes])
        for cube in neighbours_active_cells:
            n_active_around = len(get_neighbours_hyper(cube).intersection(active_hypercubes))
            if cube in active_hypercubes and n_active_around in [2, 3]:
                active_next_round.add(cube)
            elif cube not in active_hypercubes and n_active_around == 3:
                active_next_round.add(cube)

        active_hypercubes = active_next_round

    return len(active_hypercubes)


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
