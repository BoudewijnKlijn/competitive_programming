from itertools import product


CHARACTERS = "#."


def count_groups(records):
    groups = []
    current_length = 0
    for char in records:
        if char == "#":
            current_length += 1
        elif current_length:
            groups.append(current_length)
            current_length = 0
    if current_length:
        groups.append(current_length)
    return groups


def augment(records, groups):
    n_question_marks = records.count("?")
    n_damaged = sum(groups)
    n_brackets = records.count("#")
    n_bracket_replacements = n_damaged - n_brackets

    valid_options = 0
    replacements = product(CHARACTERS, repeat=n_question_marks)
    for replacement in replacements:
        # skip if bracket replacements are incorrect
        if replacement.count("#") != n_bracket_replacements:
            continue

        new_records = records
        for char in replacement:
            new_records = new_records.replace("?", char, 1)

        # check if valid
        if count_groups(new_records) == groups:
            valid_options += 1

    return valid_options


def augment_faster(records, groups):
    pass


def part1(content):
    ans = 0
    for i, line in enumerate(content.strip().split("\n")):
        records, groups = line.split()
        groups = [int(group) for group in groups.split(",")]
        ans += augment(records, groups)
    return ans


def part2(content):
    ans = 0
    for i, line in enumerate(content.strip().split("\n")):
        records, groups = line.split()

        # unfold the records and groups
        records = "?".join([records for _ in range(5)])
        groups = [int(group) for _ in range(5) for group in groups.split(",")]

        extra = augment(records, groups)
        ans += extra

    return ans


if __name__ == "__main__":

    assert count_groups("###") == [3]
    assert count_groups("##.#") == [2, 1]
    assert count_groups("##.#.") == [2, 1]
    assert count_groups("#.#.###") == [1, 1, 3]
    assert count_groups(".#...#....###.") == [1, 1, 3]

    SAMPLE = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""

    assert part1(SAMPLE) == 21

    CONTENT = open("day12.txt").read().strip()

    print(part1(CONTENT))

    # part1(CONTENT)
    # part2(CONTENT)
