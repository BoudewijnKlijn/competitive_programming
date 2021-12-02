from typing import Iterable, List, Union
import re


def load_data(filename) -> List[int]:
    with open(filename, 'r') as f:
        lines = f.read().strip()
        pattern = re.compile(r'([a-z]+) (\d+)')
        return re.findall(pattern, lines)


if __name__ == '__main__':
    input_file = 'day2.txt'
    data = load_data(input_file)


    h = 0
    v = 0
    aim = 0

    # part 1
    # for direction, units in data:
    #     units = int(units)
    #     print(direction, units)
    #     if direction in ['forward']:
    #         h += units
    #     elif direction == 'down':
    #         v += units
    #     elif direction == 'up':
    #         v -= units
    #     else:
    #         raise NotImplementedError(f'{direction} is not implemented')

    for direction, units in data:
        units = int(units)
        print(direction, units)
        if direction in ['forward']:
            h += units
            v += aim * units
        elif direction == 'down':
            aim += units
        elif direction == 'up':
            aim -= units
        else:
            raise NotImplementedError(f'{direction} is not implemented')

    print(f'horizontal: {h} vertical: {v}')
    print(f'answer: {h * v}')

