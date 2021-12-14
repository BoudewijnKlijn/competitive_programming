import re
from collections import Counter
from collections import defaultdict
from typing import Dict, Tuple


def load_data(filename: str) -> str:
    with open(filename, 'r') as f:
        return f.read()


def parse_data(raw_data: str) -> Tuple[str, Dict[str, str]]:
    start, insertion_rules = raw_data.strip().split('\n\n')

    pattern = re.compile(r'([A-Z]+) -> ([A-Z]+)')
    pairs = re.findall(pattern, insertion_rules.strip())

    return start, dict(pairs)


def step(old_pair_counts: Dict[str, int]) -> Dict[str, int]:
    new_pair_counts = defaultdict(int)
    for pair, count in old_pair_counts.items():
        insertion = pair_insertion_rules.get(pair)
        if insertion is None:
            new_pair_counts[pair] += count
        else:
            new_pair_counts[pair[0] + insertion] += count
            new_pair_counts[insertion + pair[1]] += count
    return new_pair_counts


def init_pair_counts() -> Dict[str, int]:
    pairs = list()
    for first_letter, second_letter in zip(polymer_template[:-1], polymer_template[1:]):
        pairs.append(first_letter + second_letter)
    return Counter(pairs)


def count_individual_letters_in_pairs(pair_counts):
    letter_counts = defaultdict(int)
    for pair, count in pair_counts.items():
        first_letter = pair[0]
        letter_counts[first_letter] += count

    # We count the first letter of each pair, so we have to +1 the count of the last letter of the polymer, since it
    # is never the first letter.
    letter_counts[polymer_template[-1]] += 1

    return Counter(letter_counts)


def solve(n_steps: int) -> int:
    # Initialize pair counts.
    pair_counts = init_pair_counts()

    # Run n_steps.
    for _ in range(n_steps):
        pair_counts = step(pair_counts)

    # Determine number of occurrences of individual letters.
    letter_counts = count_individual_letters_in_pairs(pair_counts)
    most_common = letter_counts.most_common()[0][1]
    least_common = letter_counts.most_common()[-1][1]

    return most_common - least_common


if __name__ == '__main__':
    # Sample data
    RAW = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""

    # Assert solution is correct
    polymer_template, pair_insertion_rules = parse_data(RAW)
    assert solve(10) == 1588
    assert solve(40) == 2188189693529
    print('Tests pass.')

    # Actual data
    RAW = load_data('day14.txt')

    # Parse data
    polymer_template, pair_insertion_rules = parse_data(RAW)

    # Part 1
    print('Part 2:', solve(10))

    # Part 2
    print('Part 2:', solve(40))
