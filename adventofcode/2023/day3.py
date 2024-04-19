import re


def find_needle(contents, pattern):
    # return needle row, col_first, col_last, and needle itself
    locations = list()
    for row, line in enumerate(contents.split("\n")):
        numbers = re.finditer(pattern, line)
        for number in numbers:
            locations.append((row, number.start(), number.end() - 1, number.group()))
    return locations


def close_enough(number_location, character_locations):
    # check if number is close enough to a special character
    # close enough if rows differ by at most 1,
    # and column of special character is between the start and end of the number with margin of 1
    for character_location in character_locations:
        if (
            abs(number_location[0] - character_location[0]) <= 1
            and number_location[1] - 1
            <= character_location[1]
            <= number_location[2] + 1
        ):
            return True
    return False


def part1(contents):
    ans = 0

    # find location of all numbers
    number_pattern = r"\d+"
    number_locations = find_needle(contents, number_pattern)

    # find location of all special characters
    character_pattern = r"[^\d\.]"
    character_locations = find_needle(contents, character_pattern)

    # check if numbers are close enough to a special character
    for number_location in number_locations:
        if close_enough(number_location, character_locations):
            ans += int(number_location[3])

    return ans


def part2(contents):
    ans = 0

    # find location of all numbers
    number_pattern = r"\d+"
    number_locations = find_needle(contents, number_pattern)

    # find location of all special characters
    character_pattern = r"[^\d\.]"
    character_locations = find_needle(contents, character_pattern)

    # find * locations that are adjacent to exactly two numbers, and multiply those numbers
    for star_location in character_locations:
        if star_location[3] != "*":
            continue

        count_ = 0
        temp_ = 1
        for number_location in number_locations:
            if close_enough(number_location, [star_location]):
                count_ += 1
                temp_ *= int(number_location[3])
        if count_ == 2:
            ans += temp_

    return ans


if __name__ == "__main__":
    sample = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""

    assert part1(sample) == 4361

    with open("day3.txt") as f:
        contents = f.read()

    ans1 = part1(contents)
    print(ans1)

    assert part2(sample) == 467835

    ans2 = part2(contents)
    print(ans2)
