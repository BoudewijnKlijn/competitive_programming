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
    signals = []
    outputs = []
    for line in raw_data.strip().split('\n'):
        a, b = map(str.strip, line.split('|'))
        signals.append(a.split())
        outputs.append(b.split())
    #     ern = re.pattern = r'([a-z]+) | ([a-z]+)'
    # signals, outputs = re.findall(pattern, raw_data)

    return signals, outputs


if __name__ == '__main__':
    # Sample data
    RAW = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"""
    data = parse_data(RAW)
    print(data)

    # Assert solution is correct
    pass

    # Actual data
    RAW = load_data('input.txt')
    data = parse_data(RAW)

    # Part 1
    signals, outputs = data
    sum_ = 0
    for signal, output in zip(signals, outputs):
        print(signal, output)

        for i, o in enumerate(output):
            if len(Counter(o)) in [2, 3, 4, 7]:
                sum_ += 1
    print(sum_)
    print(Counter(signal))
    # Part 2

