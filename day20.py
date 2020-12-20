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

    # flip all rotations vertical (top row becomes bottom row)
    for i in range(4):
        for r_old, c_old in product(range(10), range(10)):
            orientation_mapping[4+i][(r_old, c_old)] = orientation_mapping[i][(9 - r_old, c_old)]

    return images, edges, matches, orientation_mapping


# def get_edges(image):
#     edges = set()
#     for r_or_c, zero_or_9 in product(list('rc'), [0, 9]):
#         new = ''.join([char for (r, c), char in image.items() if r_or_c == zero_or_9]
#         edges.add(new)
#         edges.add(new[::-1)
#     return edges
#

def get_edge(image, orientation=0, face=0):
    image = change_orientation(image=image, orientation=orientation)
    if face == 0:
        return ''.join([image.get((0, c)) for c in range(9)])
    elif face == 1:
        return ''.join([image.get((r, 9)) for r in range(9)])
    elif face == 2:
        return ''.join([image.get((9, c)) for c in range(9)])
    elif face == 3:
        return ''.join([image.get((r, 0)) for r in range(9)])
    else:
        raise ValueError()


def print_image(image):
    for r in range(10):
        for c in range(10):
            char = image.get((r, c))
            if char:
                print(char, end='')
        print('')


def change_orientation(image, orientation):
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


def get_adjacent_coordinates(r, c, max_r, max_c):
    dr = [-1, 0, 1, 0]
    dc = [0, 1, 0, -1]
    return [(r + drr, c + dcc) for drr, dcc in zip(dr, dc) if 0 <= r + drr < max_r and 0 <= c + dcc < max_c]


def get_image_positions():
    images, edges, matches, orientation_mapping = parsed

    # start building the image with one corner image. ignore orientation of first one, just find adjacent pieces
    for name, match in matches.items():
        if len(match) == 2:
            break

    width = 1
    while width * width < len(images):
        width += 1

    total_image = defaultdict(dict)
    for r, c, in product(range(width), range(width)):
        if (r, c) == (0, 0):
            total_image[(0, 0)]['name'] = name
            pass  # todo orientation
            continue

        # find ajacent images in total image
        adjacent_coordinates = get_adjacent_coordinates(r, c, width, width)
        images_placed_and_adjacent = [total_image.get((ac_r, ac_c)).get('name') for ac_r, ac_c in adjacent_coordinates
                                      if
                                      total_image.get((ac_r, ac_c))]

        # find __one__ adjacent image
        for name, match in matches.items():
            if len(match) == len(adjacent_coordinates) and all([im in match for im in images_placed_and_adjacent]) \
                    and name not in set([v['name'] for v in total_image.values()]):
                total_image[(r, c)]['name'] = name
                pass  # todo orientation
                break

    assert set([v['name'] for v in total_image.values()]) == set(matches.keys()), 'Not all images are used'

    return total_image


def part2():
    images, edges, matches, orientation_mapping = parsed

    # start building the image with one corner image. ignore orientation of first one, just find adjacent pieces
    total_image = get_image_positions()

    width = 1
    while width * width < len(images):
        width += 1

    # now fix orientation.
    for r, c, in product(range(width), range(width)):

        # for the top-left corner, we try all orientations with the one to the right and one to bottom
        if (r, c) == (0, 0):
            top_left_corner_image = total_image[(0, 0)]['name']
            right_of_top_left_corner_image = total_image[(0, 1)]['name']
            below_top_left_corner_image = total_image[(1, 0)]['name']

            possible_orientations = 0
            for orientation_1, orientation_2, orientation_3 in product(range(8), range(8), range(8)):
                if get_edge(images.get(top_left_corner_image), orientation_1, face=1) == \
                        get_edge(images.get(right_of_top_left_corner_image), orientation_2, face=3) and \
                        get_edge(images.get(top_left_corner_image), orientation_1, face=2) == \
                        get_edge(images.get(below_top_left_corner_image), orientation_3, face=0):

                    total_image[(0, 0)]['orientation'] = orientation_1
                    total_image[(0, 1)]['orientation'] = orientation_2
                    total_image[(1, 0)]['orientation'] = orientation_3

                    possible_orientations += 1

            assert possible_orientations == 1
            continue

        elif (r, c) == (0, 1) or (r, c) == (1, 0):
            continue

        # other images are just appended. orientation is fixed by the top-left and adjacent images.
        # first try left
        if (r, c-1) in total_image.keys():
            left_image = total_image[(r, c-1)]['name']
            left_orientation = total_image[(r, c - 1)]['orientation']
            right_image = total_image[(r, c)]['name']
            possible_orientations = 0
            for right_orientation in range(8):
                if get_edge(images.get(left_image), left_orientation, face=1) == \
                        get_edge(images.get(right_image), right_orientation, face=3):

                    total_image[(r, c)]['orientation'] = right_orientation
                    possible_orientations += 1

            assert possible_orientations == 1

        else:
            # if no left, use top
            top_image = total_image[(r - 1, c)]['name']
            top_orientation = total_image[(r - 1, c)]['orientation']
            bottom_image = total_image[(r, c)]['name']

            possible_orientations = 0
            for bottom_orientation in range(8):
                if get_edge(images.get(top_image), top_orientation, face=2) == \
                        get_edge(images.get(bottom_image), bottom_orientation, face=0):

                    total_image[(r, c)]['orientation'] = bottom_orientation
                    possible_orientations += 1

            assert possible_orientations == 1

    # print complete image
    for r, c in product(range(width), range(width)):
        print(r, c)
        print_image(change_orientation(images.get(total_image.get((r, c)).get('name')),
                                       total_image.get((r, c)).get('orientation')))


    # remove borders


    # print_image(images[2789])
    # print('\n\n')
    # im2 = change_orientation(images[2789], orientation=2)
    # print_image(im2)
    # print('\n\n')
    # im2 = change_orientation(images[2789], orientation=6)
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
