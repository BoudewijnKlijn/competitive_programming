import re


def parse_input(contents):
    games = list()
    for game in contents.split("\n"):
        # remove game prefix
        game = re.sub(r"Game \d+: ", "", game)

        # split game into sets
        sets = list()
        sets_raw = game.split(";")
        for set_ in sets_raw:
            # find number of red, green, and blue
            red = re.findall(r"(\d+) red", set_)
            red = 0 if not red else int(red[0])
            green = re.findall(r"(\d+) green", set_)
            green = 0 if not green else int(green[0])
            blue = re.findall(r"(\d+) blue", set_)
            blue = 0 if not blue else int(blue[0])
            sets.append((red, green, blue))

        games.append(sets)

    return games


def is_valid(sets, restrictions):
    for red, green, blue in sets:
        if red > restrictions[0] or green > restrictions[1] or blue > restrictions[2]:
            return False
    return True


def part1(structured, restrictions):
    ans = 0
    for i, sets in enumerate(structured, start=1):
        if is_valid(sets, restrictions):
            ans += i
    return ans


def part2(structured):
    ans = 0
    for sets in structured:
        min_red = min_green = min_blue = 0
        for r, g, b in sets:
            min_red = max(min_red, r)
            min_green = max(min_green, g)
            min_blue = max(min_blue, b)
        ans += min_red * min_green * min_blue
    return ans


if __name__ == "__main__":

    contents = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""
    structured = parse_input(contents)
    RESTRICTIONS = (12, 13, 14)

    assert part1(structured, RESTRICTIONS) == 8

    assert part2(structured) == 2286

    contents = open("day2.txt").read().strip()
    structured = parse_input(contents)
    ans1 = part1(structured, RESTRICTIONS)
    print(ans1)

    ans2 = part2(structured)
    print(ans2)
