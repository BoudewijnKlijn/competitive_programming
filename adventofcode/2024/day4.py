from collections import Counter

# all 8 directions
directions = [
    (-1, -1),  # top left
    (-1, 0),  # top
    (-1, 1),  # top right
    (0, -1),  # left
    (0, 1),  # right
    (1, -1),  # bottom left
    (1, 0),  # bottom
    (1, 1),  # bottom right
]


# only diagonal directions
diagonal_directions = [
    (-1, -1),  # top left
    (-1, 1),  # top right
    (1, -1),  # bottom left
    (1, 1),  # bottom right
]


def part1(contents):
    contents = [[char for char in line] for line in contents.split("\n")]
    R = len(contents)
    C = len(contents[0])
    ans = 0
    for row in range(R):
        for col in range(C):
            # find X to start XMAS
            if contents[row][col] == "X":
                # search in all 8 directions
                for dr, dc in directions:
                    r = row
                    c = col
                    # check if all letters are present
                    correct = True
                    for letter in "MAS":
                        r += dr
                        c += dc
                        if (
                            r < 0
                            or r >= R
                            or c < 0
                            or c >= C
                            or contents[r][c] != letter
                        ):
                            correct = False
                            break
                    # all letters are correct, add 1 to answer
                    if correct:
                        ans += 1
    return ans


def part2(contents):
    """Look for M instead of X. Then search in diagonal directions.
    If all letters of MAS present, store the location of A.
    If A is part of MAS in two different directions, then it is part of two times MAS in an X shape.
    Count the number of locations where A is present twice."""
    contents = [[char for char in line] for line in contents.split("\n")]
    R = len(contents)
    C = len(contents[0])
    A_locations = list()
    for row in range(R):
        for col in range(C):
            # find M to start MAS
            if contents[row][col] == "M":
                # search in diagonal directions
                for dr, dc in diagonal_directions:
                    r = row
                    c = col
                    # check if all letters are present
                    correct = True
                    for letter in "AS":
                        r += dr
                        c += dc
                        if (
                            r < 0
                            or r >= R
                            or c < 0
                            or c >= C
                            or contents[r][c] != letter
                        ):
                            correct = False
                            break
                    # if MAS is present. store the location of letter A
                    if correct:
                        A_locations.append((r - dr, c - dc))

    # if A is present in the same location twice, then it is part of two different MAS
    count_locations = Counter(A_locations)
    ans = 0
    for value in count_locations.values():
        if value == 2:
            ans += 1
    return ans


if __name__ == "__main__":

    sample = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""

    assert part1(sample) == 18

    with open("2024/day4.txt") as f:
        contents = f.read().strip()

    ans1 = part1(contents)
    print(ans1)

    assert part2(sample) == 9

    ans2 = part2(contents)
    print(ans2)
