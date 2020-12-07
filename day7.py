import timeit
import re


def load_data():
    with open(input_file, 'r') as f:
        data = f.read().strip().split('\n')
    return data


def parse_data(data):
    parsed = dict()
    for line in data:
        line = line.replace(' bags', '').replace(' bag', '')
        main_bag, contents_part = map(str.strip, line.split('contain'))
        contents = list(map(str.strip, re.findall('[a-z ]{2,}', contents_part)))
        counts = list(map(int, map(str.strip, re.findall(r'[\d]', contents_part))))
        if len(contents) == 1 and 'no other' in contents[0]:
            contents = list()
        parsed.update({main_bag: dict(zip(contents, counts))})
    return parsed


def part1():
    possible = set()
    needles = ['shiny gold']
    while needles:
        needle = needles.pop(0)
        for k, v in parsed.items():
            if needle in v:
                needles.append(k)
                possible.add(k)

    return len(possible)


def get_number_of_bags(needle):
    contents = parsed.get(needle)
    total = 0
    for needle, count in contents.items():
        total += count + count * get_number_of_bags(needle)
    return total


# if len(contents) == 0:
#     return 1
# else:


def part2():
    return get_number_of_bags('shiny gold')


def main():
    a1 = part1()
    print(a1)

    a2 = part2()
    print(a2)


if __name__ == '__main__':
    input_file = 'input7.txt'
    data = load_data()
    parsed = parse_data(data)
    main()

    # t = timeit.Timer('part1(data)', globals=globals())
    # n = 10000
    # print(sum(t.repeat(repeat=n, number=1)) / n)
