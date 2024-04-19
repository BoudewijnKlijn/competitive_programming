import re


DIGITS = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
    # reverse letters for the second pattern
    "eno": "1",
    "owt": "2",
    "eerht": "3",
    "ruof": "4",
    "evif": "5",
    "xis": "6",
    "neves": "7",
    "thgie": "8",
    "enin": "9",
}


def part1(contents):
    total = 0
    for line in contents.split("\n"):
        digits = re.findall(r"\d", line)
        first_digit = int(digits[0])
        last_digit = int(digits[-1])
        total += first_digit * 10 + last_digit

    return total


def part2(contents):
    total = 0
    for line in contents.split("\n"):

        pattern = r"\d|one|two|three|four|five|six|seven|eight|nine"
        digits = re.findall(pattern, line)
        digits = [DIGITS.get(d, d) for d in digits]
        first_digit = int(digits[0])

        # reverse the string to search from the back
        pattern2 = r"\d|enin|thgie|neves|xis|evif|ruof|eerht|owt|eno"
        digits = re.findall(pattern2, line[::-1])
        digits = [DIGITS.get(d, d) for d in digits]
        # since we reversed the string, the last digit is now the first
        last_digit = int(digits[0])

        total += first_digit * 10 + last_digit

    return total


if __name__ == "__main__":

    sample = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""

    assert part1(sample) == 142

    with open("day1.txt") as f:
        contents = f.read().strip()

    ans1 = part1(contents)
    print(ans1)

    sample2 = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""

    assert part2(sample2) == 281

    ans2 = part2(contents)
    print(ans2)
