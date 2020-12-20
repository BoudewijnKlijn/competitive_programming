import timeit
import re
from itertools import product
from collections import defaultdict
from collections import Counter


def load_data():
    with open(input_file, 'r') as f:
        data = f.read().strip().split('\n\n')
    return data


def parse_data():
    images = defaultdict(dict)
    for tile in data:
        name = None
        for r, line in enumerate(tile.split('\n'), start=-1):
            if 'Tile' in line:
                name = int(re.search(r'\d+', line)[0])
                continue
            for c, char in enumerate(line):
                images[name][(r, c)] = char

    edges = defaultdict(dict)
    for name, image in images.items():
        edges[name]['normal'] = list()

        edges[name]['normal'].append(''.join([char for (r, c), char in image.items() if r == 0]))
        edges[name]['normal'].append(''.join([char for (r, c), char in image.items() if r == 9]))
        edges[name]['normal'].append(''.join([char for (r, c), char in image.items() if c == 0]))
        edges[name]['normal'].append(''.join([char for (r, c), char in image.items() if c == 9]))

        edges[name]['reversed'] = list()
        for edge in edges[name]['normal']:
            edges[name]['reversed'].append(edge[::-1])

    matches = defaultdict(set)
    for name, edge_type in edges.items():
        for name2, edge_type2 in edges.items():
            if name == name2:
                continue

            for edge1, edge2 in product(edge_type['normal'] + edge_type['reversed'],
                                        edge_type2['normal'] + edge_type2['reversed']):
                if edge1 == edge2:
                    matches[name].add(name2)

    # an image can be in 8 different orientations. create mappings to go from input data to each orientation
    orientation_mapping = defaultdict(dict)
    for r_old, c_old in product(range(10), range(10)):
        # no change
        orientation_mapping[0][(r_old, c_old)] = (r_old, c_old)

        # rotate right (1x, 2x, 3x)
        orientation_mapping[1][(r_old, c_old)] = (c_old, 9 - r_old)
        orientation_mapping[2][(r_old, c_old)] = (9 - r_old, 9 - c_old)
        orientation_mapping[3][(r_old, c_old)] = (9 - c_old, r_old)

    # flip all rotations vertical (top becomes bottom)
    for i in range(4):
        for r_old, c_old in product(range(10), range(10)):
            orientation_mapping[4+i][(r_old, c_old)] = orientation_mapping[i][(9 - r_old, 9 - c_old)]

    return images, edges, matches, orientation_mapping


def print_image(image):
    for r in range(10):
        for c in range(10):
            char = image.get((r, c))
            # print(char)
            if char:
                print(char, end='')
        print('')


def rotate_image(image, orientation=5):
    images, edges, matches, orientation_mapping = parsed
    new_image = dict()
    for r_old, c_old in image.keys():
        r_new, c_new = orientation_mapping[orientation].get((r_old, c_old))
        new_image[(r_new, c_new)] = image.get((r_old, c_old))
    return new_image


def part1():
    _, _, matches, _ = parsed

    ans = 1
    n_matches = list()
    for name, match in matches.items():
        if len(match) == 2:
            ans *= name
        n_matches.append(len(match))
    # print(Counter(n_matches))
    return ans


def part2():
    images, edges, matches, orientation_mapping = parsed

    # start building the image with one corner image. ignore orientation of first one, just find adjacent pieces
    for name, match in matches.items():
        if len(match) == 2:
            break

    total_image = defaultdict(dict)
    for r, c, in product(range(12), range(12)):
        # print(r, c)
        if r == 0 and c == 0:
            total_image[(r, c)]['name'] = name
            pass  # todo orientation
            continue

        # find ajacent images in total image
        dr = [-1, 0, 1, 0]
        dc = [0, 1, 0, -1]
        adjacent_coordinates = [(r+drr, c+dcc) for drr, dcc in zip(dr, dc) if 0 <= r+drr <= 11 and 0 <= c+dcc <= 11]
        images_placed_and_adjacent = [total_image.get((ac_r, ac_c)).get('name') for ac_r, ac_c in adjacent_coordinates if
                                      total_image.get((ac_r, ac_c))]

        for name, match in matches.items():
            # print(match)
            if len(match) == len(adjacent_coordinates) and all([im in match for im in images_placed_and_adjacent]) \
                    and name not in set([v['name'] for v in total_image.values()]):
                total_image[(r, c)]['name'] = name
                pass  # todo orientation
                break

    assert set([v['name'] for v in total_image.values()]) == set(matches.keys())

    # print(orientation_mapping[1])
    #
    # print_image(images[2789])
    # print('\n\n')
    # im2 = rotate_image(images[2789])
    # print_image(im2)


def main():
    a1 = part1()
    print(a1)

    a2 = part2()
    print(a2)


if __name__ == '__main__':
    input_file = 'input20.txt'
    data = load_data()
    parsed = parse_data()
    main()

    # t = timeit.Timer('part2()', globals=globals())
    # n = 10
    # print(sum(t.repeat(repeat=n, number=1)) / n)
