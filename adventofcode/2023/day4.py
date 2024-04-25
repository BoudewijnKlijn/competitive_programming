import re
from collections import defaultdict


def part1(contents, n):
    ans = 0
    for line in contents.split("\n"):
        numbers = re.findall(r"\d+", line)[1:]

        winning, have = set(numbers[:n]), set((numbers[n:]))
        n_overlap = len(winning.intersection(have))

        if n_overlap >= 1:
            ans += 2 ** (n_overlap - 1)

    return ans


def part2(contents, n):
    d = defaultdict(int)
    for i, line in enumerate(contents.split("\n"), start=1):
        d[i] += 1  # the original card
        numbers = re.findall(r"\d+", line)[1:]

        winning, have = set(numbers[:n]), set((numbers[n:]))
        n_overlap = len(winning.intersection(have))

        for x in range(n_overlap):
            d[i + 1 + x] += d[i]  # the copies

    return sum(d.values())


if __name__ == "__main__":

    sample = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""

    assert part1(sample, 5) == 13

    with open("day4.txt") as f:
        contents = f.read().strip()

    ans = part1(contents, 10)
    print(ans)

    assert part2(sample, 5) == 30

    ans = part2(contents, 10)
    print(ans)
