import timeit


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
    return lines


mapping = {
    # dx, dy, dz
    'ne': (1, 0, -1),
    'e': (1, -1, 0),
    'se': (0, -1, 1),
    'sw': (-1, 0, 1),
    'w': (-1, 1, 0),
    'nw': (0, 1, -1),
}


def part1():

    lines = parsed
    black_tiles = set()
    for line in lines:
        x, y, z = (0, 0, 0)
        for move in line:
            dx, dy, dz = mapping.get(move)
            x, y, z = x+dx, y+dy, z+dz
        if (x, y, z) not in black_tiles:
            black_tiles.add((x, y, z))
        else:
            black_tiles.remove((x, y, z))
    return len(black_tiles)





def part2():
    pass


def main():
    a1 = part1()
    print(a1)

    a2 = part2()
    print(a2)


if __name__ == '__main__':
    input_file = 'input24.txt'
    data = load_data()
    parsed = parse_data()
    main()

    # t = timeit.Timer('part2_regex()', globals=globals())
    # n = 10
    # print(sum(t.repeat(repeat=n, number=1)) / n)
