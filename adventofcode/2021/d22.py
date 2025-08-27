from dataclasses import dataclass
import re
from typing import Set
from itertools import product
from copy import deepcopy


def load_data(filename: str) -> str:
    with open(filename, 'r') as f:
        return f.read()


def parse_data(raw_data: str):
    pattern = re.compile(r'(on|off) x=([\-\d]+)..([\-\d]+),y=([\-\d]+)..([\-\d]+),z=([\-\d]+)..([\-\d]+)')
    return pattern.findall(raw_data.strip())


def make_cubes(x1, x2, y1, y2, z1, z2, b1=-50, b2=50):
    cubes = set()
    if b1 and b2:
        x1 = max(x1, b1)
        x2 = min(x2, b2)
        y1 = max(y1, b1)
        y2 = min(y2, b2)
        z1 = max(z1, b1)
        z2 = min(z2, b2)

    for x in range(x1, x2+1):
        for y in range(y1, y2+1):
            for z in range(z1, z2+1):
                cubes.add((x, y, z))
    return cubes


def part1():
    on_cubes = set()
    for line in data:
        line_cubes = make_cubes(*map(int, line[1:]))
        if line[0] == 'on':
            on_cubes.update(line_cubes)
        elif line[0] == 'off':
            on_cubes -= line_cubes
    return len(on_cubes)


@dataclass
class Cube:
    x1: int
    x2: int
    y1: int
    y2: int
    z1: int
    z2: int

    def __eq__(self, other):
        return self.x1 == other.x1 and self.x2 == other.x2 and self.y1 == other.y1 and self.y2 == other.y2 and \
               self.z1 == other.z1 and self.z2 == other.z2

    def __hash__(self):
        return hash((self.x1, self.x2, self.y1, self.y2, self.z1, self.z2))

    def volume(self):
        return (self.x2 - self.x1 + 1) * (self.y2 - self.y1 + 1) * (self.z2 - self.z1 + 1)

    def subtract(self, other: 'Cube') -> Set['Cube']:
        """Subtract another Cube from this Cube. Return all resulting cubes."""
        # If other doesn't overlap anywhere, return set with self.
        if other.x2 < self.x1 or self.x2 < other.x1 or other.y2 < self.y1 or self.y2 < other.y1 or \
                other.z2 < self.z1 or self.z2 < other.z1:
            return {self}

        new_cubes = set()
        other = deepcopy(other)

        # Adjust bounds of other cube, to be at most as large as this cube.
        other.x1 = max(other.x1, self.x1)
        other.x2 = min(other.x2, self.x2)
        other.y1 = max(other.y1, self.y1)
        other.y2 = min(other.y2, self.y2)
        other.z1 = max(other.z1, self.z1)
        other.z2 = min(other.z2, self.z2)

        left = (self.x1, other.x1 - 1)
        mid_x = (other.x1, other.x2)
        right = (other.x2 + 1, self.x2)
        bottom = (self.y1, other.y1 - 1)
        mid_y = (other.y1, other.y2)
        top = (other.y2 + 1, self.y2)
        front = (self.z1, other.z1 - 1)
        mid_z = (other.z1, other.z2)
        back = (other.z2 + 1, self.z2)
        for x, y, z in product([left, mid_x, right], [bottom, mid_y, top], [front, mid_z, back]):
            if x == mid_x and y == mid_y and z == mid_z:
                # Do not add the other cube.
                continue

            # Only add a cube if all dimensions are non-negative.
            if x[0] <= x[1] and y[0] <= y[1] and z[0] <= z[1]:
                new_cubes.add(Cube(*x, *y, *z))

        return new_cubes


assert Cube(0, 0, 0, 0, 0, 0).volume() == 1
assert Cube(0, 1, 0, 1, 0, 1).volume() == 8
assert Cube(0, 2, 0, 2, 0, 2).volume() == 27

assert Cube(0, 0, 0, 0, 0, 0).subtract(Cube(0, 0, 0, 0, 0, 0)) == set()
assert Cube(0, 0, 0, 0, 0, 0).subtract(Cube(1, 1, 1, 1, 1, 1)) == {Cube(0, 0, 0, 0, 0, 0)}


def part2():
    on_cubes = set()
    for i, line in enumerate(data):
        new_cube = Cube(*map(int, line[1:]))
        if not on_cubes:
            on_cubes.add(new_cube)
            continue

        new_on_cubes = set()
        # Even when we add a new cube, we have to subtract that from the existing cubes, to avoid double counting.
        for on_cube in on_cubes:
            new_on_cubes.update(on_cube.subtract(new_cube))
        if line[0] == 'on':
            # Add the new cube.
            new_on_cubes.add(new_cube)

        on_cubes = new_on_cubes
    return sum(c.volume() for c in on_cubes)


if __name__ == '__main__':
    # Sample data
    RAW = """on x=10..12,y=10..12,z=10..12
on x=11..13,y=11..13,z=11..13
off x=9..11,y=9..11,z=9..11
on x=10..10,y=10..10,z=10..10"""

    # Assert solution is correct
    data = parse_data(RAW)
    assert part1() == 39

    RAW = """on x=-20..26,y=-36..17,z=-47..7
on x=-20..33,y=-21..23,z=-26..28
on x=-22..28,y=-29..23,z=-38..16
on x=-46..7,y=-6..46,z=-50..-1
on x=-49..1,y=-3..46,z=-24..28
on x=2..47,y=-22..22,z=-23..27
on x=-27..23,y=-28..26,z=-21..29
on x=-39..5,y=-6..47,z=-3..44
on x=-30..21,y=-8..43,z=-13..34
on x=-22..26,y=-27..20,z=-29..19
off x=-48..-32,y=26..41,z=-47..-37
on x=-12..35,y=6..50,z=-50..-2
off x=-48..-32,y=-32..-16,z=-15..-5
on x=-18..26,y=-33..15,z=-7..46
off x=-40..-22,y=-38..-28,z=23..41
on x=-16..35,y=-41..10,z=-47..6
off x=-32..-23,y=11..30,z=-14..3
on x=-49..-5,y=-3..45,z=-29..18
off x=18..30,y=-20..-8,z=-3..13
on x=-41..9,y=-7..43,z=-33..15"""
# on x=-54112..-39298,y=-85059..-49293,z=-27449..7877
# on x=967..23432,y=45373..81175,z=27513..53682"""

    # Assert solution is correct
    data = parse_data(RAW)
    assert part1() == 590784

    RAW = load_data('day22_sample.txt')
    data = parse_data(RAW)
    assert part2() == 2758514936282235
    print('All tests pass.')

    # Actual data
    RAW = load_data('day22.txt')
    data = parse_data(RAW)

    # Part 1
    print(f'Part 1 {part1()}')

    # Part 2
    print(f'Part 2 {part2()}')
