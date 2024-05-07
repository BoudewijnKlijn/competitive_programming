def get_path_length(galaxy1, galaxy2):
    return abs(galaxy1[0] - galaxy2[0]) + abs(galaxy1[1] - galaxy2[1])


def get_sum_shortest_paths(galaxies):
    sum_shortest_paths = 0
    for i, galaxy1 in enumerate(galaxies):
        for galaxy2 in galaxies[i + 1 :]:
            sum_shortest_paths += get_path_length(galaxy1, galaxy2)
    return sum_shortest_paths


def expand_universe(universe, expansion_constant):
    insert_rows = list()
    insert_cols = list()

    for r, row in enumerate(universe):
        if all(cell == "." for cell in row):
            insert_rows.append(r)
    for c in range(len(universe[0])):
        if all(row[c] == "." for row in universe):
            insert_cols.append(c)

    # insert from the back so that the indices are not affected
    for r in reversed(insert_rows):
        for _ in range(expansion_constant):
            universe.insert(r, ["."] * len(universe[0]))
    for row in universe:
        for c in reversed(insert_cols):
            for _ in range(expansion_constant):
                row.insert(c, ".")
    return universe


def get_galaxies(universe):
    galaxies = list()
    for r, row in enumerate(universe):
        for c, cell in enumerate(row):
            if cell == "#":
                galaxies.append((r, c))
    return galaxies


def part1(content, expansion_constant=2):
    universe = [list(line) for line in content.strip().split("\n")]
    universe2 = expand_universe(universe, expansion_constant=expansion_constant - 1)
    galaxies = get_galaxies(universe2)

    return get_sum_shortest_paths(galaxies)


def part2(content, expansion_constant=2):
    """Two ways of solving (neither would insert 1 million rows/columns):
    1. for each empty row/col insert 1, then 2, then 3, and then derive the formula
    2. in the shortest path calculation use a variable for empty rows/cols"""

    sequence = [part1(content, expansion_constant=i) for i in range(1, 4)]
    diff = [n2 - n1 for n1, n2 in zip(sequence, sequence[1:])]
    assert all(diff[0] == n for n in diff)

    return sequence[0] + diff[0] * (expansion_constant - 1)


if __name__ == "__main__":

    SAMPLE = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""

    assert (part1(SAMPLE)) == 374

    CONTENT = open("day11.txt").read().strip()

    print(part1(CONTENT))

    assert (part2(SAMPLE, expansion_constant=10)) == 1030
    assert (part2(SAMPLE, expansion_constant=100)) == 8410

    expansion = 1_000_000

    print(part2(CONTENT, expansion_constant=expansion))
