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


def determine_line_type_and_simplify(line: str) -> Tuple[str, str]:
    """A corrupt line has a __wrong__ character at some place.
    An incomplete line has a __missing__ character. It might consist of only opening tags.
    Remove correct characters iteratively. Correct characters are combinations of counterpart keys and values."""

    while line:
        # Incomplete line consists of only opening tags.
        if all(char in COUNTERPART.keys() for char in line):
            return 'incomplete', line

        # Simplify line by removing correct characters.
        for i1, (char1, char2) in enumerate(zip(line[:-1], line[1:])):
            if COUNTERPART[char1] == char2:
                # Remove correct characters, a combination of counterpart key and value.
                line = line[:i1] + line[i1+2:]
                break
            elif char2 in COUNTERPART.values():
                # Corrupt line: char2 is a closing char (because COUNTERPART value), but it not the correct counterpart.
                return 'corrupt', line

    raise ValueError('Should never get here. Line is correct but it should be corrupt or incomplete.')


def find_corrupt_char_and_simplify(line: str) -> Tuple[str, str]:
    """The first corrupt char has to be a closing char that doesn't match the opening char."""
    for i1, (char1, char2) in enumerate(zip(line[:-1], line[1:])):
        if char2 in COUNTERPART.keys():
            continue
        # Remove the corrupt char and the preceding opening char and return the remaining line.
        return char2, line[:i1] + line[i1+2:]


POINTS = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}

POINTS2 = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
}


def part1():
    """Determine line type, either corrupt or incomplete.
    Do nothing with incomplete lines.
    Correct corrupt lines and calculate score based on corrupt characters."""
    score = 0
    for line in data:
        while line:
            line_type, line = determine_line_type_and_simplify(line)
            if line_type == 'corrupt':
                # Make the line correct by removing the corrupt characters.
                corrupt_char, line = find_corrupt_char_and_simplify(line)
                score += POINTS[corrupt_char]
            if line_type == 'incomplete':
                # Ignore incomplete lines. Continue with the next line.
                break
    return score


def part2():
    """Remove corrupt lines and complete the incomplete lines.
    Incomplete lines can easily be completed by adding the counterparts in reverse order."""
    scores = list()
    for line in data:
        score = 0
        while line:
            line_type, line = determine_line_type_and_simplify(line)
            if line_type == 'corrupt':
                # Remove the corrupt lines, which is the same as score += 0 and continue with the next line.
                break
            if line_type == 'incomplete':
                # Loop through line characters in reverse order
                for closing_char in line[::-1]:
                    score = score * 5 + POINTS2[COUNTERPART[closing_char]]
                scores.append(score)
                break

    return sorted(scores)[len(scores) // 2]


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
    assert part1() == 26397
    assert part2() == 288957

    # Actual data
    RAW = load_data('day10.txt')
    data = parse_data(RAW)

    # Part 1
    print(f'Part 1: {part1()}')

    # Part 2
    print(f'Part 2: {part2()}')
