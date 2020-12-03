import timeit


def load_data():
    with open(input_file, 'r') as f:
        data = f.read().strip().split()
    return data


def part1(data, move_x=3, move_y=1):
    trip = str()
    x, y = 0, 0
    width = len(data[0])

    while y < len(data):
        # get symbol
        symbol = data[y][x % width]
        trip += symbol

        # move to next
        y += move_y
        x += move_x

    return trip.count('#')


def part2(data):
    moves = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]  # (x ,y)

    ans2 = 1
    for move_x, move_y in moves:
        n_trees = part1(data, move_x, move_y)
        ans2 *= n_trees
    return ans2


def main():
    a1 = part1(data)
    print(a1)

    a2 = part2(data)
    print(a2)


if __name__ == '__main__':
    input_file = 'input3.txt'
    data = load_data()
    main()

    # t = timeit.Timer('par1(data)', globals=globals())
    # n = 10000
    # print(sum(t.repeat(repeat=n, number=1)) / n)
