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
    #     ern = re.pattern = r'([a-z]+)\s| ([a-z]+)'
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

    RAW = """acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf"""

    data = parse_data(RAW)
    # print(data)

    # Assert solution is correct
    pass

    # Actual data
    RAW = load_data('input.txt')
    data = parse_data(RAW)

    # Part 1
    signals, outputs = data
    sum_ = 0
    for signal, output in zip(signals, outputs):
        for i, o in enumerate(output):
            if len(Counter(o)) in [2, 3, 4, 7]:
                sum_ += 1
    print(sum_)

    # Part 2


    #  aaaa
    # b    c
    # b    c
    #  dddd
    # e    f
    # e    f
    #  gggg

    # make mapping: use positions above and map each letter to a number


    signals, outputs = data

    sum_ = 0

    digit_mapping = {
        'abcefg': '0',
        'cf': '1',
        'acdeg': '2',
        'acdfg': '3',
        'bcdf': '4',
        'abdfg': '5',
        'abdefg': '6',
        'acf': '7',
        'abcdefg': '8',
        'abcdfg': '9',
    }
    answer = 0

    # First decode easy number to get letters in mapping
    for signal, output in zip(signals, outputs):
        mapping = {letter: None for letter in list('abcdefg')}
        # print(mapping)
        lengths = defaultdict(list)
        for i, s in enumerate(signal):
            lengths[len(s)].append(s)
        # print(lengths)

        output_to_signal = dict()
        signal_to_output = dict()

        # the easy input length
        signal_to_output[1] = lengths[2][0]
        signal_to_output[4] = lengths[4][0]
        signal_to_output[7] = lengths[3][0]
        signal_to_output[8] = lengths[7][0]

        # print(signal_to_output)
        # exit()

        # A: get mapping for a: not in signal 7, but in signal 1
        mapping['a'] = (set(signal_to_output[7]) - set(signal_to_output[1])).pop()

        counts = Counter(''.join([*signal]))

        # B: get mapping for b: it occurs 6 times in all signals
        tmp = [k for k, v in counts.items() if v == 6]
        assert len(tmp) == 1, 'B length must be 1'
        mapping['b'] = tmp.pop()

        # E: get mapping for e: it occurs 4 times in all signals
        tmp = [k for k, v in counts.items() if v == 4]
        assert len(tmp) == 1, 'E length must be 1'
        mapping['e'] = tmp.pop()

        # F: get mapping for f: it occurs 9 times in all signals
        tmp = [k for k, v in counts.items() if v == 9]
        assert len(tmp) == 1, 'F length must be 1'
        mapping['f'] = tmp.pop()

        # C: get mapping for c: it occurs 8 times in all signals, and it cannot be A
        eights_counts = set([k for k, v in counts.items() if v == 8])
        assert len(eights_counts) == 2, 'C length must be 2'
        tmp = eights_counts - {mapping['a']}
        assert len(tmp) == 1, 'C2 length must be 1'
        mapping['c'] = tmp.pop()

        # G: get mapping for g: it occurs 7 times in all signals, and it cannot be signal with length 4
        seven_counts = set([k for k, v in counts.items() if v == 7])
        assert len(seven_counts) == 2, 'G length must be 2'
        tmp = seven_counts - set(list(signal_to_output[4]))
        assert len(tmp) == 1, 'G2 length must be 1'
        mapping['g'] = tmp.pop()

        # D: get mapping for d: it occurs 7 times in all signals, and it cannot be g
        tmp = seven_counts - {mapping['g']}
        assert len(tmp) == 1, 'D length must be 1'
        mapping['d'] = tmp.pop()

        # print(mapping)
        reverse_mapping = {v: k for k, v in mapping.items()}

        # with the mapping we can convert the outputs
        string_digit = ''
        for out in output:
            # print('out', out)
            # convert letters in output via mapping to real letters
            real_letters = ''.join([reverse_mapping[l] for l in out])
            # print(real_letters)

            # convert real letters to a digit
            sorted_letters = ''.join(sorted(list(real_letters)))
            # print('sorted', sorted_letters)
            string_digit += digit_mapping[sorted_letters]

        sum_ += int(string_digit)
        # print(sum_)

    answer += sum_

    print(answer)
