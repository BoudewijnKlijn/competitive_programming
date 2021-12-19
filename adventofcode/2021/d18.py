from dataclasses import dataclass
import re
from typing import List, Tuple, Union, Iterable
from collections import defaultdict
from itertools import cycle
from collections import Counter
import numpy as np
from itertools import chain
from copy import deepcopy



def load_data(filename: str) -> str:
    with open(filename, 'r') as f:
        return f.read()


def parse_data(raw_data: str) -> List[int]:
    return list(map(int, raw_data.strip().split(',')))


# def reduce(data):
#     """To reduce a snailfish number, you must repeatedly do the first action in this list that applies to the snailfish
#     number:
#     - If any pair is nested inside four pairs, the leftmost such pair explodes.
#     - If any regular number is 10 or greater, the leftmost such regular number splits."""
#     # # check if we need to explode
#     # string = str(data)
#     # pointer = 0
#     # depth = 0
#     # while pointer < len(string):
#     #     if string[pointer] == '[':
#     #         depth += 1
#     #     elif string[pointer] == ']':
#     #         depth -= 1
#     #     pointer += 1
#     #     if depth > 4:
#     #         print('We must explode')
#     #         break


    # # check if we need to split
    # regular_numbers = re.findall(r'\d+', str(data))
    # if any(int(regular_number) >= 10 for regular_number in regular_numbers):
    #     print('We must split')


# def explode(data):
#     """To explode a pair, the pair's left value is added to the first regular number to the left of the exploding pair
#     (if any), and the pair's right value is added to the first regular number to the right of the exploding pair (if
#     any). Exploding pairs will always consist of two regular numbers. Then, the entire exploding pair is replaced with
#     the regular number 0."""
#     depth = 0
#     while depth < 4:
#         left, right = data
#         depth += 1


@dataclass
class Leaf:
    value: int
    depth: int

    def __str__(self):
        return f'{self.value}'


class Pair:
    def __init__(self, left: Union[Leaf, List['Pair']], right: Union[Leaf, List['Pair']], depth: int):
        self.left = left
        self.right = right
        self.depth = depth

    def __str__(self):
        return f'[{self.left}, {self.right}]'

    def __repr__(self):
        return self.__str__()

    def get_leaves(self):
        leaves = list()
        for direction in (self.left, self.right):
            if isinstance(direction, Leaf):
                leaves.append(direction)
            elif isinstance(direction, Pair):
                leaves.extend(direction.get_leaves())
            else:
                raise ValueError(f'Unknown type {type(direction)}')
        return leaves


def build_binary_tree(data_in, depth=0):
    left, right = data_in
    if isinstance(left, int):
        left = Leaf(left, depth)
    elif isinstance(left, list):
        left = build_binary_tree(left, depth + 1)
    else:
        raise ValueError(f'Unknown type {type(left)}')
    if isinstance(right, int):
        right = Leaf(right, depth)
    elif isinstance(right, list):
        right = build_binary_tree(right, depth + 1)
    else:
        raise ValueError(f'Unknown type {type(right)}')
    return Pair(left, right, depth)


# def get_leaves(pair):
#     leaves = list()
#     if isinstance(pair.left, Leaf):
#         leaves.append(pair.left)
#     elif isinstance(pair.left, Pair):
#         leaves.extend(get_leaves(pair.left))
#     else:
#         raise ValueError(f'Unknown type {type(pair.left)}')
#     if isinstance(pair.right, Leaf):
#         leaves.append(pair.right)
#     elif isinstance(pair.right, Pair):
#         leaves.extend(get_leaves(pair.right))
#     else:
#         raise ValueError(f'Unknown type {type(pair.right)}')
#     return leaves


# def build_binary_tree(data, depth=0):
#     tree = Pair(data[0], data[1], depth)
#     if isinstance(tree.left, list):
#         tree.left = build_binary_tree(tree.left, depth+1)
#     else:
#         tree.left = Leaf(tree.left, depth)
#     if isinstance(tree.right, list):
#         tree.right = build_binary_tree(tree.right, depth+1)
#     else:
#         tree.right = Leaf(tree.right, depth)
#     return tree


def explode(leaves):
    """To explode a pair, the pair's left value is added to the first regular number to the left of the exploding pair
    (if any), and the pair's right value is added to the first regular number to the right of the exploding pair (if
    any). Exploding pairs will always consist of two regular numbers. Then, the entire exploding pair is replaced with
    the regular number 0."""
    leaves = deepcopy(leaves)
    for i, (leaf1, leaf2) in enumerate(zip(leaves[:-1], leaves[1:])):
        if leaf1.depth == 4 and leaf2.depth == 4:
            if i > 0:
                leaves[i - 1].value += leaf1.value
            if i < (len(leaves) - 2):
                leaves[i + 2].value += leaf2.value
            leaves.remove(leaf1)
            leaves.remove(leaf2)
            leaves.insert(i, Leaf(0, leaf1.depth - 1))
            break
    return leaves


def split_regular(leaves):
    """To split a regular number, replace it with a pair; the left element of the pair should be the regular number
    divided by two and rounded down, while the right element of the pair should be the regular number divided by two
    and rounded up. For example, 10 becomes [5,5], 11 becomes [5,6], 12 becomes [6,6], and so on."""
    leaves = deepcopy(leaves)
    for i, leaf in enumerate(leaves):
        if leaf.value >= 10:
            leaves.remove(leaf)
            # Insert right number in leaves.
            leaves.insert(i, Leaf(leaf.value // 2 + leaf.value % 2, leaf.depth + 1))
            # Insert left number in leaves.
            leaves.insert(i, Leaf(leaf.value // 2, leaf.depth + 1))
            break
    return leaves


def reduce(leaves):
    """To reduce a snailfish number, you must repeatedly do the first action in this list that applies to the snailfish
    number:
    - If any pair is nested inside four pairs, the leftmost such pair explodes.
    - If any regular number is 10 or greater, the leftmost such regular number splits."""
    while True:
        new_leaves = explode(leaves)
        if new_leaves != leaves:
            leaves = new_leaves
            continue

        new_leaves = split_regular(leaves)
        if new_leaves != leaves:
            leaves = new_leaves
            continue

        # If nothing changed then we can stop reducing.
        return leaves


def addition(left_leaves, right_leaves):
    # Increase depth of every leaf with one.
    left_leaves = [Leaf(leaf.value, leaf.depth + 1) for leaf in left_leaves]
    right_leaves = [Leaf(leaf.value, leaf.depth + 1) for leaf in right_leaves]
    return left_leaves + right_leaves


def parse_all(data):
    lines = data.strip().split('\n')
    left_leaves = build_binary_tree(eval(lines.pop(0))).get_leaves()
    while lines:
        right_leaves = build_binary_tree(eval(lines.pop(0))).get_leaves()
        left_leaves = reduce(addition(left_leaves, right_leaves))
    return left_leaves


def get_magnitude(leaves):



if __name__ == '__main__':
    # Assert explode is correct
    SAMPLES = [
        ("[[[[[9,8],1],2],3],4]", "[[[[0,9],2],3],4]"),
        ("[7,[6,[5,[4,[3,2]]]]]", "[7,[6,[5,[7,0]]]]"),
        ("[[6,[5,[4,[3,2]]]],1]", "[[6,[5,[7,0]]],3]"),
        ("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]", "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]"),
        ("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]", "[[3,[2,[8,0]]],[9,[5,[7,0]]]]"),
    ]
    for data_in, expected in SAMPLES:
        result = explode(build_binary_tree(eval(data_in)).get_leaves())
        expected = build_binary_tree(eval(expected)).get_leaves()
        assert result == expected
    print("All explode tests pass.")

    # Assert split is correct
    SAMPLES = [
        ("[[[[0,7],4],[15,[0,13]]],[1,1]]", "[[[[0,7],4],[[7,8],[0,13]]],[1,1]]"),
    ]
    for data_in, expected in SAMPLES:
        result = split_regular(build_binary_tree(eval(data_in)).get_leaves())
        expected = build_binary_tree(eval(expected)).get_leaves()
        assert result == expected
    print("All split tests pass.")

    # Assert addition is correct
    SAMPLES = [
        ("[[[[4,3],4],4],[7,[[8,4],9]]]", "[1,1]", "[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]"),
    ]
    for raw1, raw2, expected in SAMPLES:
        left_leaves = build_binary_tree(eval(raw1)).get_leaves()
        right_leaves = build_binary_tree(eval(raw2)).get_leaves()
        result = addition(left_leaves, right_leaves)
        expected = build_binary_tree(eval(expected)).get_leaves()
        assert result == expected
    print("All addition tests pass.")

    # Assert reduce is correct
    SAMPLES = [
        ("[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]", "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"),
    ]
    for data_in, expected in SAMPLES:
        result = reduce(build_binary_tree(eval(data_in)).get_leaves())
        expected = build_binary_tree(eval(expected)).get_leaves()
        assert result == expected
    print("All reduce tests pass.")

    # Assert reading, parsing, reducing etc is correct.
    SAMPLES = [
        ("""[1,1]
[2,2]
[3,3]
[4,4]""", "[[[[1,1],[2,2]],[3,3]],[4,4]]"),
        ("""[1,1]
[2,2]
[3,3]
[4,4]
[5,5]""", "[[[[3,0],[5,3]],[4,4]],[5,5]]"),
        ("""[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]""", "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]"),
    ]
    for data_in, expected in SAMPLES:
        result = parse_all(data_in)
        expected = build_binary_tree(eval(expected)).get_leaves()
        assert result == expected
    print("All tests pass.")

    # Actual data
    # RAW = load_data('input.txt')
    # data = parse_data(RAW)

    # Part 1

    # Part 2
