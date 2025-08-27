

def load_data():
    with open(input_file, 'r') as f:
        data = f.read().strip().split('\n')
    return data


def parse_data():
    parsed = list()
    for line in data:
        operation, argument = line.split()
        parsed.append((operation, int(argument)))
    return parsed


def part1(parsed):
    accumulator = 0
    position = 0
    been = set()
    while position not in been:
        if position == len(parsed):
            return accumulator, True
        been.add(position)
        operation, argument = parsed[position]
        if operation == 'acc':
            accumulator += argument
            position += 1
        elif operation == 'jmp':
            position += argument
        elif operation == 'nop':
            position += 1

    return accumulator, False


def part2():
    for i, (operation, argument) in enumerate(parsed):
        if operation == 'nop':
            temp_parsed = parsed.copy()
            temp_parsed[i] = ('jmp', argument)
            ans, correct = part1(temp_parsed)
            if correct:
                return ans

        elif operation == 'jmp':
            temp_parsed = parsed.copy()
            temp_parsed[i] = ('nop', argument)
            ans, correct = part1(temp_parsed)
            if correct:
                return ans


def main():
    a1, _ = part1(parsed)
    print(a1)

    a2 = part2()
    print(a2)


if __name__ == '__main__':
    input_file = 'input8.txt'
    data = load_data()
    parsed = parse_data()
    main()

    # t = timeit.Timer('part1(data)', globals=globals())
    # n = 10000
    # print(sum(t.repeat(repeat=n, number=1)) / n)
