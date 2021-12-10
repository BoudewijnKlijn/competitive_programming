from dataclasses import dataclass
import re
from typing import List, Tuple, Union
from collections import defaultdict
from itertools import cycle
from collections import Counter
import numpy as np


def load_data(filename: str) -> str:
    with open(filename, 'r') as f:
        return f.read()


def parse_data(raw_data: str):
    return raw_data.strip().splitlines()


COUNTERPART = {
        '(': ')',
        '[': ']',
        '{': '}',
        '<': '>',
    }


def determine_type(line: str) -> Tuple[bool, str]:
    # an illegal line has a __wrong__ character at some place
    # an incomplete line has a __missing__ character
    # - it might consist of only opening tags
    # remove correct characters iteratvely
    # correct characters are combinations of counterparts

    line = line.strip()
    i = 0
    while line:
        remove_chars = False
        if all(char in COUNTERPART.keys() for char in line):
            return ('incomplete', line)
        i += 1
        # if i > 10:
        #     break
        print(f'before {i}: {line}')
        # simplify line
        for i1, (char1, char2) in enumerate(zip(line[:-1], line[1:])):
            if char1 not in COUNTERPART.keys():
                return ('corrupt', line)
            if COUNTERPART[char1] == char2:
                # remove correct characters
                print(i1, char1, char2)
                line = line[:i1] + line[i1+2:]
                print(f'after {i}: {line}')
                remove_chars = True
                break

        if not remove_chars:
            return ('corrupt', line)
    print('error')


def find_corrupt_char(line: str) -> str:
    # the first corrupt char has to be a closing char, but not matching the opening char
    for i1, (char1, char2) in enumerate(zip(line[:-1], line[1:])):
        if char2 not in COUNTERPART.values():
            continue
        #remove the corrupt char and the opening char and return the line
        return char2, line[:i1] + line[i1+2:]


POINTS = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}

POINTS2 = {
    '(': 1,
    '[': 2,
    '{': 3,
    '<': 4,
}

def part1():
    # find incomplete and corrupt lines
    score = 0
    for line in data:
        while line:
            print(line)
            line_type, line = determine_type(line)
            print(line_type)
            print(line)
            if line_type == 'corrupt':
                corrupt_char, line = find_corrupt_char(line)
                score += POINTS[corrupt_char]
                print(line)
            if line_type == 'incomplete':
                print(line)
                print('stop')
                break
    print(score)
    return score


def part2():
    # remove corrupt lines and complete the incomplete lines
    # since we only got opening tags we can reverse the order
    scores = list()
    for line in data:
        score = 0
        while line:
            print(line)
            line_type, line = determine_type(line)
            print(line_type)
            print(line)
            if line_type == 'corrupt':
                corrupt_char, line = find_corrupt_char(line)
                print(line)
                print('stop')
                break
            if line_type == 'incomplete':
                reversed_line = line[::-1]
                for closing_char in reversed_line:
                    score = score * 5 + POINTS2[closing_char]
                print('stop')
                scores.append(score)
                break

    print(scores)
    ans = sorted(scores)[len(scores) // 2]

    print(ans)
    return ans


if __name__ == '__main__':
    # Sample data
    RAW = """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]"""
    data = parse_data(RAW)

    # Assert solution is correct
    part1() == 26397

    # Actual data
    RAW = load_data('input.txt')
    data = parse_data(RAW)

    # Part 1
    part1()

    # Part 2
    part2()
