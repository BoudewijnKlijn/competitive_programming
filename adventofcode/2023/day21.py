

DIRECTIONS = {
    (-1, 0),  # up
    (0, 1),  # right
    (1, 0),  # down
    (0, -1),  # left
}


def move(grid, start_positions: set, part2=False):
    R, C = len(grid), len(grid[0])
    new_positions = set()
    for r, c in start_positions:
        for dr, dc in DIRECTIONS:
            new_r, new_c = r + dr, c + dc
            if grid[new_r % R][new_c % C] != "#":
                if part2 or (0 <= new_r < R and 0 <= new_c < C):
                    new_positions.add((new_r, new_c))
    return new_positions


def find_start(content):
    grid = [list(line) for line in content.strip().splitlines()]
    R, C = len(grid), len(grid[0])
    for r in range(R):
        for c in range(C):
            if grid[r][c] == "S":
                return r, c


def part1(content, steps=6, part2=False):
    """Works but too slow for part2!"""
    grid = [list(line) for line in content.strip().splitlines()]
    R, C = len(grid), len(grid[0])

    # find start and replace with .
    start = find_start(content)
    grid[start[0]][start[1]] = "."

    positions = {start}
    for _ in range(steps):
        positions = move(grid, positions, part2)

    return len(positions)


def part2(content, steps=26501365):
    """First some analysis:
    Many points cannot be reached, even if close and after many steps.
    E.g. the starting point cannot be reached, because the number of steps is odd.
    Then, let's assume there are no rocks (#) in the grid, on how many points can we land?
    The area where we can get is roughly a circle with a radius of steps, hence the area is steps^2 * pi.
    However, half cannot be covered since we would need an even number of steps.
    The sample has 121 squares of which 40 are rocks (~1/3), hence 81 are free (~2/3).
    My puzzle input has 17161 of which 1762 are rocks (~10%), hence 15399 are free (~90%).
    So my puzzle answer should be approximately: steps ** 2 * pi * 0.9 * 0.5 = ~992884826410852
    Verification with the sample and up to 5000 steps shows that the approximation overestimates ~56%.
    For more steps that overestimation should become less.
    992_884_826_410_852
    Even if it is an overestimation, there are too many cells to investigate: 992884826410852 / 1.56 = 636464632314648

    If the map wouldn't expand, the number if reachable cells would flip between and odd or even number of steps.
    Given that we do so many steps, there is a large (inner) region we don't need to investigate.
    Every cell that can be reached after odd steps, will have been reached.
    We only need to investigate areas near the outer radius.

    I made a thinking error: the area is not a circle, but a square that is tilted 45 degrees.
    The square has sides of sqrt(2) * steps; the area is 2 * steps ** 2. In that case, the approximation is close.
    So my puzzle answer should be approximately: steps ** 2 * 2 * 0.9 * 0.5 = ~632_090_112_176_902

    A tilted square is easier to calculate than a circle, since the circle expansion would be different into all angles,
    and that would need simulation with many positions to check.
    The tilted square expands into 4 directions and along each diagonal the expansion is the same.

    Without having to do manual analysis of how fast we expand into the four directions, there should be a pattern
    if we increase the steps with the length of the side of the square, starting from the same remainder.
    Determine remainder of steps divided by the side length. Then whenever we get the same remainder, save the number
    of reachable cells. Then, similar to day 9, we determine the delta a few times. Once we reach 0 a few times, we have
    the pattern. From there we can determine the end result by using the function of day 9 several times.
    """
    grid = [list(line) for line in content.strip().splitlines()]
    R, C = len(grid), len(grid[0])

    # find start and replace with .
    start = find_start(content)
    grid[start[0]][start[1]] = "."

    positions = {start}
    array = list()
    remainder = steps % R
    for s in range(1, steps):
        positions = move(grid, positions, part2=True)
        # store the number of reachable cells whenever the remainder is the same
        if s % R == remainder:
            array.append(len(positions))
            d1 = delta(array)
            d2 = delta(d1)

            # show progress
            if steps == 26501365:
                print("PROGRESS...")
                print(array)
                print(d1)
                print(d2)

            if len(d2) > 2 and d2[-1] == d2[-2] == d2[-3]:
                # found the pattern. reapply the delta function ((steps - s) // R) times to find next array element
                # keep the array small to speed things up
                for _ in range((steps - s) // R):
                    array = array[-4:] + [day9_delta(array)]
                return array[-1]


def day9_delta(sequence):
    if all(n == 0 for n in sequence[-2:]):
        return 0
    return sequence[-1] + day9_delta(
        [n2 - n1 for n1, n2 in zip(sequence, sequence[1:])]
    )


def analysis(content):
    grid = [list(line) for line in content.strip().splitlines()]
    R, C = len(grid), len(grid[0])

    start = find_start(content)
    print(f"{start=}")
    grid[start[0]][start[1]] = "."
    # in the sample and the real input, the start is on an even cell

    print(R * C, R, C)
    n_asterisk = content.count("#")
    print(f"{n_asterisk=}")

    # approximate answer
    steps = [6, 10, 50, 100, 500, 1000, 5000]
    real_answer = [16, 50, 1594, 6536, 167004, 668697, 16733044]
    for radius, correct in zip(steps, real_answer):
        # guess = radius ** 2 * pi * 2/3 * 0.5  # circle: incorrect
        guess = radius**2 * 2 * 2 / 3 * 0.5  # tilted square, seems better approximation
        # guess = radius ** 2 * 2 * 39/121  # tilted square
        print(guess / correct)

    n_asterisk_odd = 0  # how many # on odd cells
    odd_cells = 0
    even_cells = 0
    n_unreachable = []  # some cells are unreachable; surrounded by rocks
    for r in range(R):
        for c in range(C):
            if grid[r][c] == "#" and (r + c) % 2 == 1:
                n_asterisk_odd += 1
            if (r + c) % 2 == 1:
                odd_cells += 1
            else:
                even_cells += 1
            if grid[r][c] == "." and all(
                grid[(r + dr) % R][(c + dc) % C] == "#" for dr, dc in DIRECTIONS
            ):
                n_unreachable += [(r, c)]

    print(f"{n_asterisk_odd=}")
    print(f"{odd_cells=} {even_cells=}")
    print(f"{n_unreachable=}")

    # when is steady state reached?
    # Total number of occupied cells of 2 consecutive moves is R * C - n_asterisk - len(n_unreachable)
    total_consecutive = R * C - n_asterisk - len(n_unreachable)
    print(f"{total_consecutive=}")

    # occupied cells should flip between odd and even after certain (large) number of steps
    positions = {start}
    prev = 0
    for i in range(1, 1000):
        positions = move(grid, positions)
        current = len(positions)
        print(f"{i=} {current=} {current + prev=}")
        if current + prev == total_consecutive:
            print(f"Steady state after {i} moves.")
            break
        prev = current

    if i % 2 == 1:
        positions = move(grid, positions)

    for _ in range(2):
        positions = move(grid, positions)
        print("ODD")
        print(len(positions))
        positions = move(grid, positions)
        print("EVEN")
        print(len(positions))
    # Sample has 121 cells, 61 are even, 60 are odd.
    # 40 are rocks, 81 are free.
    # of the 40 rocks, 21 or on odd cells, 19 are on even cells.
    # Steady state (after large number of odd) moves: 60 - 21 = 39
    # Steady state (after large number of even) moves: 61 - 19 = 42
    # Steady state is reached after 14 moves.

    # real input has 17161 cells, 8581 are even, 8580 are odd.
    # 2 cells are unreachable, surrounded by rocks. One on even, one on odd.
    # 1762 are rocks, 15399 are free.
    # of the 1762 rocks, 952 are on odd cells, 810 are on even cells.
    # Steady state (after large number of odd) moves: 8580 - 952 - 1 = 7627
    # Steady state (after large number of even) moves: 8581 - 810 - 1 = 7770
    # Steady state is reached after 130 moves (starting from the centre).
    # The map is 131x131, and we start in the centre, which means there is not a single rock to the left, right,
    # up or down from the start.

    array = list()
    for s in range(start[0], R * R, R):
        array.append(part1(SAMPLE, steps=s, part2=True))
        print(delta(array))
        print(delta(delta(array)))
        print(delta(delta(delta(array))))


def delta(array):
    return [array[i + 1] - array[i] for i in range(len(array) - 1)]


if __name__ == "__main__":
    SAMPLE = """...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
..........."""

    assert part1(SAMPLE, steps=6) == 16

    with open("day21.txt") as f:
        CONTENT = f.read()

    print(part1(CONTENT, steps=64))

    # part 2
    assert part1(SAMPLE, steps=6, part2=True) == 16
    assert part1(SAMPLE, steps=10, part2=True) == 50
    assert part1(SAMPLE, steps=50, part2=True) == 1594
    assert part1(SAMPLE, steps=100, part2=True) == 6536
    assert part2(SAMPLE, steps=500) == 167004
    assert part2(SAMPLE, steps=1000) == 668697
    assert part2(SAMPLE, steps=5000) == 16733044

    # analysis(SAMPLE)
    # analysis(CONTENT)

    print(part2(CONTENT, steps=26501365))  # 630129824772393
