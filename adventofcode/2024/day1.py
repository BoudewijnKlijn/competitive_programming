from collections import Counter


def part1(contents):
    left = list()
    right = list()
    for line in contents.split("\n"):
        a, b = map(int, line.split())
        left.append(a)
        right.append(b)

    left.sort()
    right.sort()
    sum_diff = 0
    for a, b in zip(left, right):
        sum_diff += abs(a - b)

    return sum_diff


def part2(contents):
    left = list()
    right = list()
    for line in contents.split("\n"):
        a, b = map(int, line.split())
        left.append(a)
        right.append(b)

    left_counts = Counter(left)
    right_counts = Counter(right)
    similarity_sum = 0
    for key, count in left_counts.items():
        similarity_sum += key * count * right_counts.get(key, 0)
    return similarity_sum


if __name__ == "__main__":

    sample = """3   4
4   3
2   5
1   3
3   9
3   3"""

    assert part1(sample) == 11

    with open("2024/day1.txt") as f:
        contents = f.read().strip()

    ans1 = part1(contents)
    print(ans1)

    assert part2(sample) == 31

    ans2 = part2(contents)
    print(ans2)
