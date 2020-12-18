import timeit
import re


def load_data():
    with open(input_file, 'r') as f:
        data = f.read().strip().split('\n')
    return data


def parse_data():
    pass


def solve_left_to_right(chars):
    """Assumes no parentheses"""
    ans, modifier = None, None
    for char in chars:
        if ans is None:
            assert char not in ['+*'], 'first char expected to be integer'
            ans = int(char)
        elif char in list('+*'):
            modifier = char
        else:
            ans = ans * int(char) if modifier == '*' else ans + int(char)
    return ans


def part1():
    """Reduce line to line without parentheses first. Find, solve and replace parts between parenthesis"""
    pattern = re.compile(r'[\d]+|[\*\(\)\+]')
    total = 0
    for line in data:
        groups = pattern.findall(line)
        while '(' in groups or ')' in groups:
            parentheses = [(i, char) for i, char in enumerate(groups) if char in list('()')]
            for (i, parenthesis1), (j, parenthesis2) in zip(parentheses[:-1], parentheses[1:]):
                if parenthesis1 == '(' and parenthesis2 == ')':
                    replacement = solve_left_to_right(groups[i+1:j])
                    groups = groups[:i] + [replacement] + groups[j+1:]
                    break
        total += solve_left_to_right(groups)
    return total


def part2():
    pass


def main():
    a1 = part1()
    print(a1)

    a2 = part2()
    print(a2)


if __name__ == '__main__':
    input_file = 'input18.txt'
    data = load_data()
    parsed = parse_data()
    main()

    # t = timeit.Timer('part1(p1=False)', globals=globals())
    # n = 100
    # print(sum(t.repeat(repeat=n, number=1)) / n)
