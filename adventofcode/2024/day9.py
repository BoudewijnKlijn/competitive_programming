import re
import time
from collections import Counter, deque
from copy import deepcopy
from itertools import combinations, cycle
from math import prod
from operator import add, mul


def parse(contents):
    blocks = list()
    for i, number in enumerate(map(int, contents)):
        if i % 2 == 0:
            blocks.extend([str(i // 2)] * number)
        else:
            blocks.extend(["."] * number)
    return blocks


def parse2(contents):
    blocks = list()
    for i, number in enumerate(map(int, contents)):
        if i % 2 == 0:
            blocks.append((str(i // 2), number))
        else:
            blocks.append((".", number))
    return blocks


def part1(contents):
    blocks = parse(contents)

    # compress blocks
    lo = 0
    hi = len(blocks) - 1
    while lo < hi:
        while blocks[lo] != ".":
            lo += 1
        while blocks[hi] == ".":
            hi -= 1
        if lo < hi:
            # switch lo and hi simultaneously
            blocks[lo], blocks[hi] = blocks[hi], blocks[lo]

    return calc_checksum(blocks)


def calc_checksum(blocks):
    ans = 0
    for i, file_id in enumerate(blocks):
        if file_id == ".":
            continue
        ans += i * int(file_id)
    return ans


def part2(contents):
    blocks = parse2(contents)

    # compress blocks
    hi = len(blocks)
    while 0 < hi:
        # find block with id
        hi -= 1
        if blocks[hi][0] == ".":
            continue

        space_required = blocks[hi][1]
        # move block to space if possible
        lo = 0
        while lo < hi:
            if blocks[lo][0] == "." and blocks[lo][1] >= space_required:
                # found enough space to move it to
                new_size = blocks[lo][1] - space_required
                replacement_block = (".", space_required)
                if new_size > 0:
                    # adjust size of empty space if larger than zero
                    blocks[lo] = (".", new_size)
                    # determine new ordering. block with space remains
                    blocks = (
                        blocks[:lo]
                        + [blocks[hi]]
                        + blocks[lo:hi]
                        + [replacement_block]
                        + blocks[hi + 1 :]
                    )
                else:
                    # determine new ordering. block with space removed
                    blocks = (
                        blocks[:lo]
                        + [blocks[hi]]
                        + blocks[lo + 1 : hi]
                        + [replacement_block]
                        + blocks[hi + 1 :]
                    )
                break
            lo += 1

    # note: it is not needed to combine (adjacent) blocks with space.
    # blocks where new space is created are already processed.
    # blocks with space don't contributed to checksum.
    new_blocks = list()
    for string, count in blocks:
        for _ in range(count):
            new_blocks.append(string)
    blocks = new_blocks

    return calc_checksum(blocks)


if __name__ == "__main__":

    sample = """2333133121414131402"""

    assert part1(sample) == 1928

    with open("2024/day9.txt") as f:
        contents = f.read().strip()

    ans1 = part1(contents)
    print(ans1)

    assert part2(sample) == 2858

    ans2 = part2(contents)
    print(ans2)
