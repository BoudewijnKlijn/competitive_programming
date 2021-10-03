import timeit
from collections import defaultdict


def load_data():
    with open(input_file, 'r') as f:
        data = list(map(int, f.read().strip().split(',')))
    return data


def parse_data():
    pass


def part1(n_total=2020):
    data_copy = data.copy()
    for i in range(n_total - len(data_copy)):
        spoken = data_copy[-1]
        if spoken not in data_copy[:-1]:
            data_copy.append(0)
        else:
            # turns_apart = list(reversed(data_copy[:-1])).index(spoken) + 1
            turns_apart = data_copy[-2::-1].index(spoken) + 1
            data_copy.append(turns_apart)
    return data_copy[-1]


def part2(n_total=30000000):
    """Too slow"""
    data_copy = data.copy()
    n_spoken = len(data_copy)
    data_copy += [0] * (n_total - n_spoken)
    for i in range(n_total):
        if i < n_spoken:
            continue
        spoken = data_copy[i-1]
        if spoken not in data_copy[:i-1]:
            data_copy[i] = 0
        else:
            turns_apart = data_copy[-2::-1].index(spoken) + 1
            data_copy[i] = turns_apart
    return data_copy[-1]


def part2_faster(n_total=30000000):
    data_copy = data.copy()
    n_spoken = len(data_copy)
    last_spoken = {spoken: turn for turn, spoken in enumerate(data_copy[:-1], start=1)}
    spoken = data_copy[-1]

    for turn in range(n_spoken+1, n_total+1):
        if spoken not in last_spoken:
            last_spoken[spoken], spoken = turn - 1, 0
        else:
            last_spoken[spoken], spoken = turn - 1, turn - 1 - last_spoken[spoken]
    return spoken


def part2_faster_simpler(n_total=30000000):
    data_copy = data.copy()
    n_spoken = len(data_copy)
    spoken_dict = defaultdict(list)
    for turn, spoken in enumerate(data_copy, start=1):
        spoken_dict[spoken].append(turn)

    for turn in range(n_spoken+1, n_total+1):
        if len((turns := spoken_dict[spoken])) == 1:
            spoken = 0
            spoken_dict[spoken].append(turn)
        else:
            spoken = turns[-1] - turns[-2]
            spoken_dict[spoken].append(turn)
    return spoken


def main():
    a1 = part1()
    print(a1)

    a2 = part2_faster()
    print(a2)

    a2 = part2_faster_simpler()
    print(a2)


if __name__ == '__main__':
    input_file = 'input15.txt'
    data = load_data()
    parsed = parse_data()
    main()

    t = timeit.Timer('part2_faster(n_total=2020)', globals=globals())
    n = 1000
    print(sum(t.repeat(repeat=n, number=1)) / n)

    t = timeit.Timer('part2_faster_simpler(n_total=2020)', globals=globals())
    n = 1000
    print(sum(t.repeat(repeat=n, number=1)) / n)
