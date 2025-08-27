import re


def load_data():
    with open(input_file, 'r') as f:
        contents = f.read()

    data = list()
    for line in contents.split('\n'):
        pieces = line.split(' ')
        if len(pieces) < 2:
            break
        low, high = map(int, pieces[0].split('-'))
        letter = pieces[1][:-1]
        password = pieces[2]
        entry = {
            'low': low,
            'high': high,
            'letter': letter,
            'password': password,
        }
        data.append(entry)

    return data


def is_valid(entry):
    pattern = f'[{entry["letter"]}]{{1}}'
    found = re.findall(pattern, entry['password'])
    if entry['low'] <= len(found) <= entry['high']:
        return True


def is_valid_part2(entry):
    low_correct = entry['password'][entry['low'] - 1] == entry['letter']
    high_correct = entry['password'][entry['high'] - 1] == entry['letter']

    if low_correct + high_correct == 1:
        return True


def part1(data):
    count_valids = 0
    for entry in data:
        if is_valid(entry):
            count_valids += 1
    return count_valids


def part2(data):
    count_valids = 0
    for entry in data:
        if is_valid_part2(entry):
            count_valids += 1
    return count_valids


def main():
    a1 = part1(data)
    print(a1)

    a2 = part2(data)
    print(a2)


if __name__ == '__main__':
    input_file = 'input2.txt'
    data = load_data()
    main()

    # t = timeit.Timer('par1(data)', globals=globals())
    # n = 10000
    # print(sum(t.repeat(repeat=n, number=1)) / n)
