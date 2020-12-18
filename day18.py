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
            assert char not in list('+*'), 'first char expected to be integer'
            ans = int(char)
        elif char in list('+*'):
            modifier = char
        else:
            ans = ans * int(char) if modifier == '*' else ans + int(char)
    return ans


def get_line_total(groups):
    while '(' in groups or ')' in groups:
        parentheses = [(i, char) for i, char in enumerate(groups) if char in list('()')]
        for (i, parenthesis1), (j, parenthesis2) in zip(parentheses[:-1], parentheses[1:]):
            if parenthesis1 == '(' and parenthesis2 == ')':
                replacement = solve_left_to_right(groups[i + 1:j])
                groups = groups[:i] + [replacement] + groups[j + 1:]
                break
    return solve_left_to_right(groups)


def part1():
    """Reduce line to line without parentheses first. Find, solve and replace parts between parentheses"""
    pattern = re.compile(r'[\d]+|[\*\(\)\+]')
    total = 0
    for line in data:
        groups = pattern.findall(line)
        total += get_line_total(groups)
    return total


def add_parentheses(groups):
    n_plusses = groups.count('+')
    for plus_i in range(n_plusses):
        plusses = [(i, char) for i, char in enumerate(groups) if char == '+']

        # find out where to place opening parenthesis
        left_insert, _ = plusses[plus_i]
        parentheses_to_open = 0
        while True:
            left_insert -= 1
            char_left = groups[left_insert]
            if char_left not in list('()+*') and parentheses_to_open == 0:
                break
            if char_left == ')':
                parentheses_to_open += 1
            elif char_left == '(':
                parentheses_to_open -= 1
                if parentheses_to_open == 0:
                    break

        # find out where to place closing parenthesis
        right_insert, _ = plusses[plus_i]
        parentheses_to_close = 0
        while True:
            right_insert += 1
            char_right = groups[right_insert]
            if char_right not in list('()+*') and parentheses_to_close == 0:
                break
            if char_right == ')':
                parentheses_to_close -= 1
                if parentheses_to_close == 0:
                    break
            elif char_right == '(':
                parentheses_to_close += 1

        # insert parentheses
        groups = groups[:left_insert] + ['('] + groups[left_insert:right_insert+1] + [')'] + groups[right_insert+1:]
    return groups


def part2():
    """Solve part 1 after placing extra parentheses to make sure '+' is first calculated"""
    pattern = re.compile(r'[\d]+|[\*\(\)\+]')
    total = 0
    for line in data:
        groups = pattern.findall(line)
        groups = add_parentheses(groups)
        total += get_line_total(groups)
    return total


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
