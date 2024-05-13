from queue import Queue


def display(grid, energized=None):
    R, C = len(grid), len(grid[0])
    for row in grid:
        print("".join(row))

    if energized is None:
        return

    print()
    for r in range(R):
        for c in range(C):
            if (r, c) in energized:
                print("#", end="")
            else:
                print(".", end="")


def part1(content, start=(0, -1, 0, 1)):
    grid = [list(row) for row in content.strip().split("\n")]
    R, C = len(grid), len(grid[0])

    energized = set()  # (r, c)
    processed = set()  # (r, c, dr, dc)

    beam_queue = Queue()  # (r, c, dr, dc)
    beam_queue.put(start)

    while not beam_queue.empty():
        r, c, dr, dc = beam_queue.get()
        assert (dr != 0 or dc != 0) and (dr * dc == 0)  # one of both should be zero
        if (r, c, dr, dc) in processed:
            continue
        processed.add((r, c, dr, dc))

        if 0 <= r + dr < R and 0 <= c + dc < C:
            cell = grid[r + dr][c + dc]
            energized.add((r + dr, c + dc))
        else:
            continue

        if cell == ".":
            beam_queue.put((r + dr, c + dc, dr, dc))  # nothing changes, beam continues
        elif cell == "|":
            if dc == 0:
                beam_queue.put(
                    (r + dr, c + dc, dr, dc)
                )  # nothing changes, beam continues
            else:
                beam_queue.put((r + dr, c + dc, -1, 0))
                beam_queue.put((r + dr, c + dc, 1, 0))
        elif cell == "-":
            if dr == 0:
                beam_queue.put(
                    (r + dr, c + dc, dr, dc)
                )  # nothing changes, beam continues
            else:
                beam_queue.put((r + dr, c + dc, 0, -1))
                beam_queue.put((r + dr, c + dc, 0, 1))
        elif cell == "/":
            beam_queue.put((r + dr, c + dc, -dc, -dr))
        elif cell == "\\":
            beam_queue.put((r + dr, c + dc, dc, dr))

    # display(grid, energized)

    return len(energized)


def part2(content):
    grid = [list(row) for row in content.strip().split("\n")]
    R, C = len(grid), len(grid[0])

    starts = list()
    for start_c in range(C):
        for r, dr in [(-1, 1), (R, -1)]:
            starts.append((r, start_c, dr, 0))
    for start_r in range(R):
        for c, dc in [(-1, 1), (C, -1)]:
            starts.append((start_r, c, 0, dc))

    best_score = 0
    for start in starts:
        score = part1(content, start=start)
        if score > best_score:
            best_score = score
            # print(start, best_score)

    return best_score


if __name__ == "__main__":
    SAMPLE = r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|...."""

    assert part1(SAMPLE) == 46

    with open("day16.txt") as f:
        CONTENT = f.read().strip()

    print(part1(CONTENT))

    assert part2(SAMPLE) == 51

    print(part2(CONTENT))
