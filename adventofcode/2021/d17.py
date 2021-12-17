from dataclasses import dataclass
import re
from typing import List, Tuple, Union
from collections import defaultdict
from itertools import cycle, product
from collections import Counter
import numpy as np


def load_data(filename: str) -> str:
    with open(filename, 'r') as f:
        return f.read()


def parse_data(raw_data: str):
    pattern = r'[-\d]+'
    x_min, x_max, y_min, y_max = re.findall(pattern, raw_data.strip())
    return x_min, x_max, y_min, y_max


def travel_step(x_in: int, y_in: int, vx_in: int, vy_in: int) -> Tuple[int, int, int, int]:
    x_out = x_in + vx_in
    y_out = y_in + vy_in
    vx_out = vx_in
    if vx_in > 0:
        vx_out = vx_in - 1
    elif vx_in < 0:
        vx_out = vx_in + 1
    vy_out = vy_in - 1
    return x_out, y_out, vx_out, vy_out


def part1():
    valid = []
    # for initial_vx, initial_vy in [(7, 2)]: #product(range(-100, 100), repeat=2):
    for initial_vx, initial_vy in product(range(0, 40), range(70, 130)):
        vx, vy = initial_vx, initial_vy
        x, y = 0, 0
        max_altitude = None
        while vx != 0 or (x in range(int(x_min), int(x_max) + 1) and y >= int(y_min)):
            x, y, vx, vy = travel_step(x, y, vx, vy)
            if max_altitude is None or y > max_altitude:
                max_altitude = y
            if x in range(int(x_min), int(x_max) + 1) and y in range(int(y_min), int(y_max) + 1):
                valid.append((initial_vx, initial_vy, max_altitude))

    valid = sorted(valid, key=lambda v: v[2], reverse=True)

    return valid[0]


if __name__ == '__main__':
    # Sample data
    RAW = """target area: x=20..30, y=-10..-5"""
    x_min, x_max, y_min, y_max = parse_data(RAW)

    # Assert solution is correct
    # assert part1()[:2] == (6, 9)

    # Actual data
    RAW = load_data('input.txt')
    x_min, x_max, y_min, y_max = parse_data(RAW)
    print(part1())

    # Part 1

    # Part 2
