from collections import defaultdict
from itertools import product
from queue import Queue

DIRECTIONS = {
    "R": (0, 1),
    "L": (0, -1),
    "U": (-1, 0),
    "D": (1, 0),
}

MAP = {
    "0": "R",
    "1": "D",
    "2": "L",
    "3": "U",
}

MAX_ = 10_000_000  # to run part 2
# MAX_ = 10  # for visualizing the sample


def get_dimensions(dug_positions):
    min_r, max_r, min_c, max_c = 0, 0, 0, 0
    for r, c in dug_positions:
        min_r = min(min_r, r)
        max_r = max(max_r, r)
        min_c = min(min_c, c)
        max_c = max(max_c, c)
    return min_r, max_r, min_c, max_c


def get_dimensions_blocks(blocks):
    min_r, max_r, min_c, max_c = 0, 0, 0, 0
    for r1, c1, r2, c2 in blocks:
        min_r = min(min_r, r1)
        max_r = max(max_r, r2)
        min_c = min(min_c, c1)
        max_c = max(max_c, c2)
    return min_r, max_r, min_c, max_c


def display(path):
    min_r, max_r, min_c, max_c = get_dimensions(path)
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            if (r, c) in path:
                print("#", end="")
            else:
                print(".", end="")
        print()


def display_blocks(blocks, vary_symbols=False):
    min_r, max_r, min_c, max_c = get_dimensions_blocks(blocks)
    grid = [["." for _ in range(min_c, max_c + 1)] for _ in range(min_r, max_r + 1)]

    if vary_symbols:
        symbols = "1234567890abcdefghijklmnopqrstuvwxyz"
    else:
        symbols = len(blocks) * "#"
    for (r1, c1, r2, c2), symbol in zip(blocks, symbols):
        for r in range(r1, r2 + 1):
            for c in range(c1, c2 + 1):
                grid[r][c] = symbol

    for row in grid:
        print("".join(row))


def get_neighbors(r, c):
    return [
        (r - 1, c),
        (r + 1, c),
        (r, c - 1),
        (r, c + 1),
    ]


def get_enclosed_area(dug_positions):
    min_r, max_r, min_c, max_c = get_dimensions(dug_positions)

    all_positions = set(product(range(min_r, max_r + 1), range(min_c, max_c + 1)))
    to_investigate = all_positions - dug_positions
    while to_investigate:
        is_enclosed = True
        new_group = set()
        queue = Queue()
        queue.put(to_investigate.pop())
        while not queue.empty():
            cell = queue.get()
            new_group.add(cell)
            neighbors = get_neighbors(*cell)
            for neighbor in neighbors:
                if neighbor not in all_positions:
                    is_enclosed = False
                if neighbor in to_investigate:
                    to_investigate.remove(neighbor)
                    queue.put(neighbor)
        if is_enclosed:
            return new_group


def part1(content):
    lines = content.strip().split("\n")

    pos = (0, 0)
    dug_positions = set()
    for line in lines:
        direction, steps, _ = line.split()
        for _ in range(int(steps)):
            pos = (pos[0] + DIRECTIONS[direction][0], pos[1] + DIRECTIONS[direction][1])
            dug_positions.add(pos)

    enclosed = get_enclosed_area(dug_positions)
    return len(dug_positions) + len(enclosed)


def part2(content):
    """Instead of thinking about single cells, we have to think about a collection of cells: blocks.
    Each block is a rectangle with a top-left corner and a bottom-right corner.
    We start with a single block that covers the entire grid.
    For each line, we split the blocks into smaller blocks, whenever a trench goes into a block.
    """
    lines = content.strip().split("\n")

    blocks = [(0, 0, 2 * MAX_, 2 * MAX_)]

    old_pos = (MAX_, MAX_)
    trenches = set()
    for line in lines:
        direction, steps, color = line.split()
        direction, steps = MAP.get(color[7]), int(color[2:7], 16)

        dr = DIRECTIONS[direction][0] * int(steps)
        dc = DIRECTIONS[direction][1] * int(steps)
        new_pos = (old_pos[0] + dr, old_pos[1] + dc)

        trench = (
            min(old_pos[0], new_pos[0]),
            min(old_pos[1], new_pos[1]),
            max(old_pos[0], new_pos[0]),
            max(old_pos[1], new_pos[1]),
        )
        trenches.add(trench)
        new_blocks = list()
        for block in blocks:
            new_blocks.extend(split_block(block, trench))
        blocks = new_blocks
        old_pos = new_pos

    assert old_pos == (MAX_, MAX_)  # we should end up at the starting position

    enclosed = group_blocks(blocks, trenches)

    # trenches overlap in the corners, so we have to subtract the number of trenches
    ans = sum((area(block) for block in enclosed | trenches)) - len(trenches)
    return ans


def split_block(block, trench):
    """Each block can at most be divided into 9 smaller blocks.
    Some blocks may lie outside the original block. Those blocks will not be added.
    Blocks with illegal dimensions will not be added."""
    r1_block, c1_block, r2_block, c2_block = block
    r1_trench, c1_trench, r2_trench, c2_trench = trench

    # no interaction between block and trench, return original block
    if (
        r1_block > r2_trench
        or r2_block < r1_trench
        or c1_block > c2_trench
        or c2_block < c1_trench
    ):
        return [block]

    assert r1_block <= r2_block
    assert c1_block <= c2_block
    assert r1_trench <= r2_trench
    assert c1_trench <= c2_trench
    new_r1s = [
        min(r1_block, r1_trench),
        max(r1_block, r1_trench),
        min(r2_block, r2_trench) + 1,
    ]
    new_r2s = [
        max(r1_block, r1_trench) - 1,
        min(r2_block, r2_trench),
        max(r2_block, r2_trench),
    ]
    new_c1s = [
        min(c1_block, c1_trench),
        max(c1_block, c1_trench),
        min(c2_block, c2_trench) + 1,
    ]
    new_c2s = [
        max(c1_block, c1_trench) - 1,
        min(c2_block, c2_trench),
        max(c2_block, c2_trench),
    ]
    new_blocks = list()
    for r1, r2 in zip(new_r1s, new_r2s):
        for c1, c2 in zip(new_c1s, new_c2s):
            if r1 > r2 or c1 > c2:
                continue

            # new block must be inside the original block
            if r1_block <= r1 and r2 <= r2_block and c1_block <= c1 and c2 <= c2_block:
                new_blocks.append((r1, c1, r2, c2))

    # area of new blocks must be equal to area of original block
    assert area(block) == sum(area(new_block) for new_block in new_blocks)

    return new_blocks


def area(block):
    return (block[2] - block[0] + 1) * (block[3] - block[1] + 1)


def get_block_neighbors(blocks):
    neighbors = defaultdict(set)
    for block1 in blocks:
        for block2 in blocks:
            if block1 == block2:
                continue

            # add block to neighbors if blocks are adjacent
            # overlap in rows, and columns are adjacent
            is_overlap_rows = max(block1[0], block2[0]) <= min(block1[2], block2[2])
            is_adjacent_cols = (
                max(block1[1], block2[1]) == min(block1[3], block2[3]) + 1
            )
            if is_overlap_rows and is_adjacent_cols:
                neighbors[block1].add(block2)
                neighbors[block2].add(block1)
            # overlap in columns, and rows are adjacent
            is_overlap_cols = max(block1[1], block2[1]) <= min(block1[3], block2[3])
            is_adjacent_rows = (
                max(block1[0], block2[0]) == min(block1[2], block2[2]) + 1
            )
            if is_overlap_cols and is_adjacent_rows:
                neighbors[block1].add(block2)
                neighbors[block2].add(block1)

    return neighbors


def is_block_part_of_trench(block, trenches):
    for trench in trenches:
        if (
            trench[0] <= block[0]
            and trench[1] <= block[1]
            and trench[2] >= block[2]
            and trench[3] >= block[3]
        ):
            return True
    return False


def group_blocks(blocks, trenches):
    """Group blocks that are adjacent to each other."""
    neighbors_dict = get_block_neighbors(blocks)

    all_positions = set(blocks)
    trench_blocks = set(
        [block for block in blocks if is_block_part_of_trench(block, trenches)]
    )
    to_investigate = all_positions - trench_blocks

    # display_blocks(trenches, vary_symbols=True)

    while to_investigate:
        is_enclosed = True
        new_group = set()
        queue = Queue()
        queue.put(to_investigate.pop())
        while not queue.empty():
            cell = queue.get()
            new_group.add(cell)
            neighbors = neighbors_dict.get(cell, set())
            for neighbor in neighbors:
                if (
                    neighbor[0] == 0
                    or neighbor[1] == 0
                    or neighbor[2] == 2 * MAX_
                    or neighbor[3] == 2 * MAX_
                ):
                    is_enclosed = False
                if neighbor in to_investigate:
                    to_investigate.remove(neighbor)
                    queue.put(neighbor)
        if is_enclosed:
            return new_group


if __name__ == "__main__":
    SAMPLE = """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)"""

    part1(SAMPLE)

    assert part1(SAMPLE) == 62

    CONTENT = open("day18.txt").read().strip()
    print(part1(CONTENT))

    assert part2(SAMPLE) == 952408144115

    print(part2(CONTENT))  # 94116351948493
