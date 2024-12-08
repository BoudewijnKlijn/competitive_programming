import re
import time
from collections import Counter, deque
from copy import deepcopy
from itertools import cycle
from math import prod
from operator import add, mul


def parse(contents):
    equations = contents.split("\n")
    answers = list()
    numbers_list = list()
    for equation in equations:
        answer, *numbers = map(int, re.findall(r"\d+", equation))
        answers.append(answer)
        numbers_list.append(numbers)
    return answers, numbers_list


def concat_ints(a, b):
    return int(str(a) + str(b))


PART1_OPERATORS = (add, mul)
PART2_OPERATORS = (*PART1_OPERATORS, concat_ints)


def part1(contents, operators=PART1_OPERATORS):
    answers, numbers_list = parse(contents)
    ans = 0
    for answer, numbers in zip(answers, numbers_list):
        intermediate_answers = set(numbers[:1])
        for number in numbers[1:]:
            tmp = set()
            for intermediate_answer in intermediate_answers:
                for operator in operators:
                    tmp.add(operator(intermediate_answer, number))
            intermediate_answers = tmp

        if answer in intermediate_answers:
            ans += answer
    return ans


def part2(contents):
    return part1(contents, PART2_OPERATORS)


if __name__ == "__main__":

    sample = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""

    assert part1(sample) == 3749

    with open("2024/day7.txt") as f:
        contents = f.read().strip()

    ans1 = part1(contents)
    print(ans1)

    assert part2(sample) == 11387

    ans2 = part2(contents)
    print(ans2)
