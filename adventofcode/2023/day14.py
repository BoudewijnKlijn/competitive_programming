def get_weight(rows):
    columns = ["".join(char) for char in zip(*rows)]
    total_weight = 0
    for col in columns:
        weight = len(col)
        for r, char in enumerate(col):
            if char == "O":
                total_weight += weight
                weight -= 1
            elif char == "#":
                weight = len(col) - r - 1

    return total_weight


def get_weight_without_tilt(rows):
    columns = ["".join(char) for char in zip(*rows)]
    total_weight = 0
    for col in columns:
        for r, char in enumerate(col):
            if char == "O":
                total_weight += len(col) - r
    return total_weight


def part1(content):
    rows = content.split("\n")
    return get_weight(rows)


def tilt(collections):
    new_collections = list()
    for collection in collections:
        new_collection = ""
        prev = 0
        stop = False
        while not stop:
            try:
                asterisk_index = collection[prev:].index("#") + prev
                n_rolling = collection[prev:asterisk_index].count("O")
                n_free = collection[prev:asterisk_index].count(".")
                new_collection += "O" * n_rolling + "." * n_free + "#"
                prev = asterisk_index + 1
            except ValueError:
                n_rolling = collection[prev:].count("O")
                n_free = collection[prev:].count(".")
                new_collection += "O" * n_rolling + "." * n_free
                stop = True

        new_collections.append(new_collection)

    return new_collections


def find_pattern(weights):
    # Start at the last element since the first element may not be part of the cycle.
    test_n_cycles = 3  # test for at least so many cycles
    for cycle_length in range(1, len(weights)):
        perfect = True
        for i in range(len(weights) - 1 - cycle_length):
            if weights[-i - cycle_length - 1] != weights[-i - 1]:
                perfect = False
                break
            if i > cycle_length * test_n_cycles:
                break
        if perfect:
            return cycle_length


def part2(content):
    """1 billion cycles is too much to simulate. We need to find a pattern."""
    collections = content.split("\n")

    weights = list()

    N = 1000
    for i in range(N):
        if i % 4 == 0:
            # add weights after (before) each full cycle
            weight = get_weight_without_tilt(collections)
            weights.append(weight)

            collections = ["".join(char) for char in zip(*collections)]
            collections = tilt(collections)
            collections = ["".join(char) for char in zip(*collections)]
        elif i % 4 == 1:
            collections = tilt(collections)
        elif i % 4 == 2:
            collections = ["".join(char) for char in zip(*collections)]
            collections = [collection[::-1] for collection in collections]
            collections = tilt(collections)
            collections = [collection[::-1] for collection in collections]
            collections = ["".join(char) for char in zip(*collections)]
        elif i % 4 == 3:
            collections = [collection[::-1] for collection in collections]
            collections = tilt(collections)
            collections = [collection[::-1] for collection in collections]

    cycle_length = find_pattern(weights)
    remainder = (1_000_000_000 - N // 4) % cycle_length

    return weights[-(cycle_length - remainder)]


if __name__ == "__main__":

    SAMPLE = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""

    SAMPLE2 = """1234
5678
abcd
efgh"""

    assert part1(SAMPLE) == 136

    assert find_pattern([1, 1, 1, 1, 1, 1, 1]) == 1

    with open("day14.txt") as f:
        CONTENT = f.read().strip()

    print(part1(CONTENT))

    assert part2(SAMPLE) == 64

    print(part2(CONTENT))
