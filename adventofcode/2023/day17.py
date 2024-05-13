from queue import PriorityQueue


DIRECTIONS = {(0, 1), (1, 0), (0, -1), (-1, 0)}


def part1(content, ultra=False):
    """Flood the grid.
    Can only turn left, right, or go straight.
    At most 3 times straight in a row."""
    grid = [[int(num) for num in row] for row in content.strip().split("\n")]
    R, C = len(grid), len(grid[0])

    queue = (
        PriorityQueue()
    )  # (heat loss, straight counter, (current r, current c), (prev dr, prev dc))
    queue.put((grid[0][1], 1, (0, 1), (0, 1)))
    queue.put((grid[1][0], 1, (1, 0), (1, 0)))

    processed = set()  # (r, c, n_straight, (prev dr, prev dc))
    while not queue.empty():
        heat_loss, n_straight, (r, c), (prev_dr, prev_dc) = queue.get()

        # Skip if already processed.
        if (r, c, n_straight, (prev_dr, prev_dc)) in processed:
            continue
        processed.add((r, c, n_straight, (prev_dr, prev_dc)))

        for dr, dc in DIRECTIONS:
            if (dr, dc) == (-prev_dr, -prev_dc):
                continue  # Not allowed to go back.

            if not ultra:
                if n_straight >= 3 and (dr, dc) == (prev_dr, prev_dc):
                    continue  # Not allowed to go straight more than 3 times.
            else:
                # Ultra mode
                if n_straight >= 10 and (dr, dc) == (prev_dr, prev_dc):
                    continue  # Not allowed to go straight more than 10 times.
                if n_straight < 4 and (dr, dc) != (prev_dr, prev_dc):
                    continue  # Must go straight at least 4 times.

            new_r, new_c = r + dr, c + dc
            if 0 <= new_r < len(grid) and 0 <= new_c < len(grid[0]):
                new_heat_loss = heat_loss + grid[new_r][new_c]
                new_n_straight = n_straight + 1 if (dr, dc) == (prev_dr, prev_dc) else 1
                queue.put((new_heat_loss, new_n_straight, (new_r, new_c), (dr, dc)))

        # Because we are using a priority queue, we can return the heat loss when we reach the end.
        if (r, c) == (R - 1, C - 1):
            if not ultra:
                return heat_loss
            if (
                ultra and n_straight >= 4
            ):  # Can only stop after at least 4 straight moves.
                return heat_loss


if __name__ == "__main__":
    SAMPLE = """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533"""

    SAMPLE2 = """111111111111
999999999991
999999999991
999999999991
999999999991"""

    assert part1(SAMPLE) == 102

    CONTENT = open("day17.txt").read().strip()
    print(part1(CONTENT))

    assert part1(SAMPLE, ultra=True) == 94
    assert part1(SAMPLE2, ultra=True) == 71

    print(part1(CONTENT, ultra=True))
