import re


def solve(time, record_distance):
    n_ways = 0
    for charge_seconds in range(time + 1):
        travel_time = time - charge_seconds
        travel_distance = charge_seconds * travel_time
        if travel_distance > record_distance:
            n_ways += 1

    return n_ways


def part1(content):
    lines = content.split("\n")
    times = list(map(int, lines[0].split()[1:]))
    distances = list(map(int, lines[1].split()[1:]))

    ans = 1
    for time, distance in zip(times, distances):
        ans *= solve(time, distance)

    return ans


def part2(content):
    # Remove whitespace which moves all digits together. Then extract the two numbers.
    time, distance = [int(x) for x in re.findall(r"\d+", re.sub(r"\s", "", content))]

    return solve(time, distance)


if __name__ == "__main__":

    SAMPLE = """Time:      7  15   30
Distance:  9  40  200"""

    assert part1(SAMPLE) == 288

    with open("day6.txt") as f:
        CONTENT = f.read().strip()

    print(part1(CONTENT))

    assert part2(SAMPLE) == 71503

    print(part2(CONTENT))
