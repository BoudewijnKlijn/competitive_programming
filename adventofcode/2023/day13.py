def find_reflection(rows):
    row_length = len(rows[0])
    columns = ["".join(x) for x in zip(*rows)]
    col_length = len(rows)

    answers = list()

    # check vertical reflection
    for left_col in range(row_length - 1):
        perfect_reflection = True
        for i in range(row_length):
            if left_col - i < 0 or left_col + 1 + i >= row_length:
                break
            if columns[left_col - i] != columns[left_col + 1 + i]:
                perfect_reflection = False
        if perfect_reflection:
            answers.append(left_col + 1)

    # check horizontal reflection
    for top_row in range(col_length - 1):
        perfect_reflection = True
        for i in range(col_length):
            if top_row - i < 0 or top_row + 1 + i >= col_length:
                break
            if rows[top_row - i] != rows[top_row + 1 + i]:
                perfect_reflection = False
        if perfect_reflection:
            answers.append((top_row + 1) * 100)

    return answers


def part1(content):
    puzzles = content.strip().split("\n\n")

    ans = 0
    for puzzle in puzzles:
        rows = puzzle.strip().split("\n")
        summary = find_reflection(rows)
        ans += summary[0]
    return ans


def part2(content):
    puzzles = content.strip().split("\n\n")

    ans = 0
    for i, puzzle in enumerate(puzzles):

        rows = puzzle.strip().split("\n")
        part2_summary = set()
        part1_summary = set(find_reflection(rows))

        for r in range(len(rows)):
            for c in range(len(rows[0])):
                tmp = rows.copy()

                # switch character in cell
                if tmp[r][c] == "#":
                    tmp[r] = tmp[r][:c] + "." + tmp[r][c + 1 :]
                else:
                    tmp[r] = tmp[r][:c] + "#" + tmp[r][c + 1 :]

                summary = find_reflection(tmp)
                part2_summary.update(summary)

        ans += sum(part2_summary - part1_summary)
    return ans


if __name__ == "__main__":
    SAMPLE = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""
    assert part1(SAMPLE) == 405

    CONTENT = open("day13.txt").read().strip()

    print(part1(CONTENT))

    print(part2(CONTENT))
