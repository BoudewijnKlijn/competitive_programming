import re
from typing import List, Tuple


def load_data(filename) -> List[Tuple[str, int]]:
    with open(filename, 'r') as f:
        lines = f.read().strip()
        pattern = re.compile(r'([a-z]+) (\d+)')
        return re.findall(pattern, lines)


def part1(input_data: List[Tuple[str, int]]) -> int:
    h = 0
    v = 0

    for direction, units in input_data:
        units = int(units)
        if direction == 'forward':
            h += units
        elif direction == 'down':
            v += units
        elif direction == 'up':
            v -= units
        else:
            raise NotImplementedError(f'{direction} is not implemented')

    return h * v


def part2(input_data: List[Tuple[str, int]]) -> int:
    h = 0
    v = 0
    aim = 0

    for direction, units in input_data:
        units = int(units)
        if direction == 'forward':
            h += units
            v += aim * units
        elif direction == 'down':
            aim += units
        elif direction == 'up':
            aim -= units
        else:
            raise NotImplementedError(f'{direction} is not implemented')

    return h * v


if __name__ == '__main__':
    input_file = 'day2.txt'
    data = load_data(input_file)

    print(f'Part 1: {part1(data)}')
    print(f'Part 2: {part2(data)}')
