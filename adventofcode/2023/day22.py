import json
import re


def overlap(x11, x12, x21, x22):
    return min(max(x21, x22), max(x11, x12)) >= max(min(x21, x22), min(x11, x12))


def lower(blocks):
    print("Lowering...")
    blocks = sorted(blocks, key=lambda x: x[2])
    new_blocks = list()
    for block in blocks:
        go_lower = True
        x1, y1, z1, x2, y2, z2 = block
        while go_lower:
            # stop if the ground is 1 level lower
            if z1 - 1 == 0:
                break

            # we only need to check blocks that are lower
            # the blocks in blocks are higher or same height so cannot intersect when going lower
            for other_block in new_blocks:
                ox1, oy1, oz1, ox2, oy2, oz2 = other_block
                if (
                    overlap(x1, x2, ox1, ox2)
                    and overlap(y1, y2, oy1, oy2)
                    and overlap(z1 - 1, z2 - 1, oz1, oz2)
                ):
                    # not possible to go lower, intersect with other block
                    go_lower = False
                    break
            else:
                # no intersect with any block, so we can lower the block and try again
                z1 -= 1
                z2 -= 1
        new_blocks.append((x1, y1, z1, x2, y2, z2))

    return new_blocks


def support(blocks):
    """Determine to how many blocks this block gives support.
    Support is given if the block is directly above another block.
    Which means overlap in x and y, and z differs by 1"""
    print("Determining support...")
    supports = {i: list() for i in range(len(blocks))}
    supported_by = {i: list() for i in range(len(blocks))}
    for i, block in enumerate(blocks):
        for j, other_block in enumerate(blocks[i + 1 :], start=i + 1):
            x1, y1, z1, x2, y2, z2 = block
            ox1, oy1, oz1, ox2, oy2, oz2 = other_block
            if (
                overlap(x1, x2, ox1, ox2)
                and overlap(y1, y2, oy1, oy2)
                and overlap(z1, z2, oz1 - 1, oz2 - 1)
            ):
                supports[i].append(j)
                supported_by[j].append(i)

    # export once for part 2, to avoid recalculating
    # json.dump(supports, open("day22_supports_sample.json", "w"))
    # json.dump(supported_by, open("day22_supported_by_sample.json", "w"))
    # json.dump(supports, open("day22_supports.json", "w"))
    # json.dump(supported_by, open("day22_supported_by.json", "w"))

    disintegrate = set(range(len(blocks)))
    is_only_support = set()
    for k, v in supported_by.items():
        if len(v) == 1:
            is_only_support.update(v)

    return len(disintegrate - is_only_support)


def part1(content):
    blocks = list()
    for line in content.strip().split("\n"):
        x1, y1, z1, x2, y2, z2 = map(int, re.findall(r"\d+", line))

        # make sure lowest part is first, to order correctly later
        if z1 > z2:
            x1, y1, z1, x2, y2, z2 = x2, y2, z2, x1, y1, z1

        blocks.append((x1, y1, z1, x2, y2, z2))

    blocks = lower(blocks)
    return support(blocks)


def part2():
    # supports = json.load(open("day22_supports_sample.json"))
    # supported_by = json.load(open("day22_supported_by_sample.json"))
    supports = json.load(open("day22_supports.json"))
    supported_by = json.load(open("day22_supported_by.json"))

    n_blocks_fall = {i: 0 for i in range(len(supported_by))}
    for block_i in range(len(supported_by)):
        fallen = {block_i}

        to_check = set(supports[str(block_i)])
        check_again = True
        while check_again:
            check_again = False
            for x in to_check:
                if x in fallen:
                    continue
                if all(vv in fallen for vv in supported_by[str(x)]):
                    fallen.add(x)
                    check_again = True
                    to_check.update(supports[str(x)])
                    break
        n_blocks_fall[block_i] = len(fallen) - 1
    return sum(n_blocks_fall.values())


if __name__ == "__main__":
    SAMPLE = """1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9"""

    assert part1(SAMPLE) == 5

    with open("day22.txt") as f:
        CONTENT = f.read().strip()

    print(part1(CONTENT))  # 524

    print(part2())  # 77070
