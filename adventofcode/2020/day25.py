import timeit


def load_data():
    with open(input_file, 'r') as f:
        data = f.read().strip().split('\n')
    return data


def transform(loop_size, subject_number=7):
    return pow(subject_number, loop_size, 20201227)


def search(loop_size=0, value=1, keys=None):
    while value not in keys:
        loop_size += 1
        value = value * 7 % 20201227
    return value, loop_size


def part1():
    pub1, pub2 = map(int, data)

    value, loop_size = search(keys={pub1, pub2})
    subject_number = pub2 if value == pub1 else pub1

    return transform(loop_size=loop_size, subject_number=subject_number)


def main():
    a1 = part1()
    print(a1)


if __name__ == '__main__':
    input_file = 'input25.txt'
    data = load_data()
    main()

    # t = timeit.Timer('part1()', globals=globals())
    # n = 10
    # print(sum(t.repeat(repeat=n, number=1)) / n)
