from collections import defaultdict


def convert(step, current_value=0):
    for char in step:
        current_value += ord(char)
        current_value *= 17
        current_value %= 256
    return current_value


def part1(content):
    steps = content.split(",")
    ans = 0
    for step in steps:
        ans += convert(step)
    return ans


def part2(content):
    steps = content.split(",")
    boxes = defaultdict(list)
    for step in steps:
        if "=" in step:
            parts = step.split("=")
        else:
            parts = step.split("-")

        box = convert(parts[0])
        if not parts[1]:
            # remove the label if present
            for spot in boxes[box]:
                if spot[0] == parts[0]:
                    boxes[box].remove(spot)
                    break
        else:
            # add or update the label
            for spot in boxes[box]:
                if spot[0] == parts[0]:
                    spot[1] = int(parts[1])
                    break
            else:
                boxes[box].append([parts[0], int(parts[1])])

    ans = 0
    for box, spots in boxes.items():
        for i, spot in enumerate(spots, start=1):
            ans += (1 + box) * i * spot[1]
    return ans


if __name__ == "__main__":
    SAMPLE = """rn=1"""

    assert convert(SAMPLE) == 30

    SAMPLE2 = """rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"""

    assert part1(SAMPLE2) == 1320

    CONTENT = open("day15.txt", "r").read().strip()

    print(part1(CONTENT))

    assert part2(SAMPLE2) == 145

    print(part2(CONTENT))
