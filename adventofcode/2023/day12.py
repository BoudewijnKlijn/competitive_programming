from functools import cache
from itertools import product

CHARACTERS = "#."


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
        groups = tuple([int(group) for _ in range(5) for group in groups.split(",")])

        extra = augment_faster(records, groups, preceding_brackets=0)
        ans += extra

    return ans


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


assert count_groups("###") == [3]
assert count_groups("##.#") == [2, 1]
assert count_groups("##.#.") == [2, 1]
assert count_groups("#.#.###") == [1, 1, 3]
assert count_groups(".#...#....###.") == [1, 1, 3]


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


def get_current_groups(records, current_length=0):
    """Check records until a question mark is found.
    Return the groups which are certain (current groups), the consecutive number of brackets
    directly before the question mark, and the remaining records."""
    current_groups = []
    for i, char in enumerate(records):
        if char == "?":
            return tuple(current_groups), current_length, records[i:]
        if char == "#":
            current_length += 1
        elif current_length:
            current_groups.append(current_length)
            current_length = 0
    if current_length:
        current_groups.append(current_length)
    return tuple(current_groups), 0, ""


assert get_current_groups("###") == ((3,), 0, "")
assert get_current_groups("##.#") == ((2, 1), 0, "")
assert get_current_groups("##.#.") == ((2, 1), 0, "")
assert get_current_groups("#.#.###") == ((1, 1, 3), 0, "")
assert get_current_groups(".#...#....###.") == ((1, 1, 3), 0, "")
assert get_current_groups("?") == (tuple(), 0, "?")
assert get_current_groups("#?") == (tuple(), 1, "?")
assert get_current_groups("#.#?") == ((1,), 1, "?")
assert get_current_groups("#.#???#.?") == ((1,), 1, "???#.?")


def is_valid(records, true_groups, preceding_brackets):
    """All current groups should be exactly equal to the true groups."""
    current_groups, leftover_brackets, new_records = get_current_groups(
        records, preceding_brackets
    )
    return current_groups == true_groups


@cache
def augment_faster(records, groups, preceding_brackets):
    """Recursively replace question marks with # or . and check if the groups are correct.
    Use a cache to prevent identical function evaluations."""

    if (len(groups) == 0 and preceding_brackets > 0) or (
        len(groups) > 0 and preceding_brackets > groups[0]
    ):
        # impossible to be correct
        return 0

    # find first question mark. if no more question marks, check if valid
    first_question_mark = records.find("?")
    if first_question_mark == -1:
        if is_valid(records, groups, preceding_brackets):
            return 1
        else:
            return 0

    # replace the first question mark with a # or .
    possible_options = 0
    for replacement in CHARACTERS:
        # replace the question mark in records
        tmp_records = (
            records[:first_question_mark]
            + replacement
            + records[first_question_mark + 1 :]
        )

        # determine the discovered groups, the leftover brackets and the new records
        current_groups, leftover_brackets, new_records = get_current_groups(
            tmp_records, preceding_brackets
        )

        # number of discovered groups cannot be greater than true number of groups
        n_current_groups = len(current_groups)
        if n_current_groups > len(groups):
            continue

        # check if the discovered groups match the true groups
        for i, current_group in enumerate(current_groups):
            if current_group != groups[i]:
                break
        else:
            # only keep the unchecked groups
            new_remaining_groups = groups[n_current_groups:]
            possible_options += augment_faster(
                new_records, new_remaining_groups, leftover_brackets
            )
    return possible_options


if __name__ == "__main__":
    SAMPLE = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""

    assert part1(SAMPLE) == 21

    CONTENT = open("day12.txt").read().strip()

    print(part1(CONTENT))

    assert part2(SAMPLE) == 525152

    print(part2(CONTENT))
