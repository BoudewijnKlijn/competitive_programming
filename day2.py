import timeit
import math


def load_data():
    with open(input_file, 'r') as f:
        contents = list(map(int, f.read().strip().split()))
    return contents


def part1(data):
    pass


def part2(data):
    pass


def main():
    a1 = part1(data)
    print(a1)



if __name__ == '__main__':
    input_file = 'input2.txt'
    data = load_data()
    main()

    # t = timeit.Timer('par1(data)', globals=globals())
    # n = 10000
    # print(sum(t.repeat(repeat=n, number=1)) / n)
