import re
from collections import Counter
from math import prod


def part1(contents):
    pattern = r"mul\(\d+,\d+\)"
    muls = re.findall(pattern, contents)
    ans_sum = 0
    for mul in muls:
        ints = re.findall(r"\d+", mul)
        ans_sum += prod(map(int, ints))
    return ans_sum


def part2(contents):
    contents = contents.replace("\n", "")

    mul_pattern = r"mul\(\d+,\d+\)"
    do_pattern = r"do\(\)"
    dont_pattern = r"don't\(\)"

    ans_sum = 0
    pos = 0
    enabled = True
    while True:
        # find first match
        mul = re.search(mul_pattern, contents[pos:])

        # stop iteration of no more matches
        if mul is None:
            break

        # check for presence of do or dont before the match
        do = re.search(do_pattern, contents[pos : pos + mul.start()])
        dont = re.search(dont_pattern, contents[pos : pos + mul.start()])

        # determine if enabled should be changed
        if dont is None and do is None:
            pass
        elif dont is not None and do is None:
            enabled = False
        elif dont is None and do is not None:
            enabled = True
        elif dont.start() > do.start():
            enabled = False
        else:
            enabled = True

        # if enabled, add
        if enabled:
            ints = re.findall(r"\d+", mul.group())
            ans_sum += prod(map(int, ints))

        # increase position to end of last match
        pos += mul.end()
    return ans_sum


if __name__ == "__main__":

    sample = (
        """xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"""
    )

    assert part1(sample) == 161

    with open("2024/day3.txt") as f:
        contents = f.read().strip()

    ans1 = part1(contents)
    print(ans1)

    assert part2(sample) == 48

    ans2 = part2(contents)
    print(ans2)
