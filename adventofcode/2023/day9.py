def delta(sequence, part2=False):
    if all(n == 0 for n in sequence):
        return 0

    if part2:
        return sequence[0] - delta(
            [n2 - n1 for n1, n2 in zip(sequence, sequence[1:])], part2
        )
    return sequence[-1] + delta([n2 - n1 for n1, n2 in zip(sequence, sequence[1:])])


def part1(content, part2=False):
    lines = content.strip().split("\n")
    sequences = [list(map(int, line.split())) for line in lines]
    return sum(delta(sequence, part2) for sequence in sequences)


if __name__ == "__main__":
    SAMPLE = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""

    assert part1(SAMPLE) == 114

    with open("day9.txt") as f:
        CONTENT = f.read().strip()

    print(part1(CONTENT))

    assert part1(SAMPLE, part2=True) == 2

    print(part1(CONTENT, part2=True))
