import numpy as np


def parse_input(contents):
    parts = contents.strip().split("\n\n")
    seeds = [int(i) for i in parts[0].split()[1:]]
    seed_to_soil = [list(map(int, i.split())) for i in parts[1].split("\n")[1:]]
    soil_to_fertilizer = [list(map(int, i.split())) for i in parts[2].split("\n")[1:]]
    fertilizer_to_water = [list(map(int, i.split())) for i in parts[3].split("\n")[1:]]
    water_to_light = [list(map(int, i.split())) for i in parts[4].split("\n")[1:]]
    light_to_temperature = [list(map(int, i.split())) for i in parts[5].split("\n")[1:]]
    temperature_to_humidity = [
        list(map(int, i.split())) for i in parts[6].split("\n")[1:]
    ]
    humidity_to_location = [list(map(int, i.split())) for i in parts[7].split("\n")[1:]]
    mappings = [
        seed_to_soil,
        soil_to_fertilizer,
        fertilizer_to_water,
        water_to_light,
        light_to_temperature,
        temperature_to_humidity,
        humidity_to_location,
    ]

    return (
        seeds,
        seed_to_soil,
        soil_to_fertilizer,
        fertilizer_to_water,
        water_to_light,
        light_to_temperature,
        temperature_to_humidity,
        humidity_to_location,
        mappings,
    )


def part1(contents):
    (
        seeds,
        seed_to_soil,
        soil_to_fertilizer,
        fertilizer_to_water,
        water_to_light,
        light_to_temperature,
        temperature_to_humidity,
        humidity_to_location,
        mappings,
    ) = parse_input(contents)

    min_location = np.inf

    for src in seeds:
        for mapping in mappings:
            for dest_range_start, src_range_start, range_length in mapping:
                if src_range_start <= src <= src_range_start + range_length:
                    src = dest_range_start + src - src_range_start
                    break

        if src < min_location:
            min_location = src

    return min_location


def part2_naive(contents):
    (
        seeds,
        *_,
        mappings,
    ) = parse_input(contents)

    min_location = np.inf

    for start, range_ in zip(seeds[::2], seeds[1::2]):
        for src in range(start, start + range_):
            for mapping in mappings:
                for dest_range_start, src_range_start, range_length in mapping:
                    if src_range_start <= src <= src_range_start + range_length:
                        src = dest_range_start + src - src_range_start
                        break

            if src < min_location:
                min_location = src

    return min_location


def part2(contents):
    # keep ranges and split up into smaller ranges
    (
        seeds,
        *_,
        mappings,
    ) = parse_input(contents)

    starts_and_ranges = sorted(zip(seeds[::2], seeds[1::2]))

    for mapping in mappings:
        adjusted = set()
        for dest_range_start, src_range_start, range_length in mapping:
            to_be_adjusted = set()
            for start_and_range in starts_and_ranges:
                leftovers, overlap = adjust_ranges(
                    *start_and_range, dest_range_start, src_range_start, range_length
                )
                adjusted.update(overlap)
                to_be_adjusted.update(leftovers)

            starts_and_ranges = list(to_be_adjusted)

        starts_and_ranges.extend(adjusted)

    return sorted(starts_and_ranges)[0][0]


def adjust_ranges(start1, range1, dest_range_start, start2, range2):
    end1 = start1 + range1 - 1
    end2 = start2 + range2 - 1

    # Mapping is before or after the seed range.
    if start2 > end1 or end2 < start1:
        return [(start1, range1)], []

    # Overlap.
    overlap = [
        (
            dest_range_start + max(start1, start2) - start2,
            min(end1, end2) - max(start1, start2) + 1,
        )
    ]
    leftovers = list()

    # Some left over on the left.
    if start1 < start2:
        leftovers.append((start1, start2 - start1))

    # Some left over on the right.
    if end2 < end1:
        leftovers.append((end2 + 1, end1 - end2))

    return leftovers, overlap


if __name__ == "__main__":

    sample = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""

    assert part1(sample) == 35

    CONTENTS = open("day5.txt").read()

    print(part1(CONTENTS))

    assert part2_naive(sample) == 46

    # print(part2_naive(CONTENTS))  # too slow

    assert part2(sample) == 46

    print(part2(CONTENTS))
