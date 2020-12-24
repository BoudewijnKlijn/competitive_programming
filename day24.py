import timeit
from itertools import product


def load_data():
    with open(input_file, 'r') as f:
        data = f.read().strip().split('\n')
    return data


def parse_data():
    lines = list()
    for line in data:
        new_line = list()
        line = list(line)
        while line:
            char = line.pop(0)
            if char in list('ns'):
                char += line.pop(0)
            new_line.append(char)
        lines.append(new_line)

    black_tiles = set()
    for line in lines:
        x, y, z = (0, 0, 0)
        for move in line:
            dx, dy, dz = mapping.get(move)
            x, y, z = x + dx, y + dy, z + dz

        if (x, y, z) not in black_tiles:
            black_tiles.add((x, y, z))
        else:
            black_tiles.remove((x, y, z))
    return black_tiles


mapping = {
    # dx, dy, dz
    'ne': (1, 0, -1),
    'e': (1, -1, 0),
    'se': (0, -1, 1),
    'sw': (-1, 0, 1),
    'w': (-1, 1, 0),
    'nw': (0, 1, -1),
}


adjacent_offset = set()
for dx, dy, dz in product(range(-1, 2), range(-1, 2), range(-1, 2)):
    if sum([dx, dy, dz]) == 0 and (dx, dy, dz) != (0, 0, 0):
        adjacent_offset.add((dx, dy, dz))


def get_adjacent_tiles(x, y, z):
    return set([(x+dx, y+dy, z+dz) for (dx, dy, dz) in adjacent_offset])


def part2():
    black_tiles = parsed
    for _ in range(100):
        new_black_tiles = set()
        test_tiles = set()
        for bt in black_tiles:
            test_tiles.update(get_adjacent_tiles(*bt))

        for test_tile in test_tiles:
            adjacent_tiles = get_adjacent_tiles(*test_tile)
            n_adjacent_black = len(adjacent_tiles.intersection(black_tiles))
            if test_tile in black_tiles and n_adjacent_black in [1, 2]:
                new_black_tiles.add(test_tile)
            elif test_tile not in black_tiles and n_adjacent_black == 2:
                new_black_tiles.add(test_tile)

        black_tiles = new_black_tiles

    return len(black_tiles)


def main():
    a1 = len(parsed)
    print(a1)

    a2 = part2()
    print(a2)


if __name__ == '__main__':
    input_file = 'input24.txt'
    data = load_data()
    parsed = parse_data()
    main()

    # t = timeit.Timer('part2()', globals=globals())
    # n = 10
    # print(sum(t.repeat(repeat=n, number=1)) / n)
