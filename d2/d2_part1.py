"""
sum(True for itm in open('d2/input.txt').read().split() if Counter(Counter(itm).values()).get(3)) *
        sum(True for itm in open('d2/input.txt').read().split() if Counter(Counter(itm).values()).get(2))
"""

import time
from collections import Counter


def read_file(filename):
    with open(filename, 'r') as f:
        return f.read()


def contains_double_or_triple(strings):
    number_of_doubles, number_of_triples = 0, 0
    for line_item in strings.split():
        if Counter(Counter(line_item).values()).get(2):
            number_of_doubles += 1
        if Counter(Counter(line_item).values()).get(3):
            number_of_triples += 1
    return number_of_doubles, number_of_triples


def main():
    contents = read_file('input.txt')
    doubles, triples = contains_double_or_triple(contents)
    answer = doubles*triples
    print(f"Answer: {answer}")


if __name__ == "__main__":
    start_time = time.time()
    main()
    execution_time = time.time() - start_time
    print("Execution time: {:.5f}s".format(execution_time))
