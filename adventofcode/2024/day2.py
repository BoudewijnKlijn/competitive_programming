from collections import Counter


def is_safe(levels):
    deltas = [l2 - l1 for l2, l1 in zip(levels[:-1], levels[1:])]
    if all(1 <= d <= 3 for d in deltas):
        return 1
    elif all(1 <= -d <= 3 for d in deltas):
        return 1
    return 0


def part1(contents):
    reports = list()
    for line in contents.split("\n"):
        levels = list(map(int, line.split(" ")))
        reports.append(levels)

    safe_count = 0
    for levels in reports:
        safe_count += is_safe(levels)
    return safe_count


def part2(contents):
    reports = list()
    for line in contents.split("\n"):
        levels = list(map(int, line.split(" ")))
        reports.append(levels)

    safe_count = 0
    for levels in reports:
        for i in range(len(levels)):
            safe = is_safe(levels[:i] + levels[i + 1 :])
            if safe:
                break
        safe_count += safe
    return safe_count


if __name__ == "__main__":

    sample = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""

    assert part1(sample) == 2

    with open("2024/day2.txt") as f:
        contents = f.read().strip()

    ans1 = part1(contents)
    print(ans1)

    assert part2(sample) == 4

    ans2 = part2(contents)
    print(ans2)
