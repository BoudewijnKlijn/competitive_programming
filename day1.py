import timeit
import math


def load_data():
    with open(input_file, 'r') as f:
        contents = list(map(int, f.read().strip().split()))
    return contents


def part1(data):
    goal = 2020
    for i, n1 in enumerate(data):
        for n2 in data[i:]:
            if n1 + n2 == goal:
                return n1 * n2


def part1_faster(data, goal=2020):
    s = set(data)
    for n1 in data:
        if goal - n1 in s:
            return n1, goal - n1


def part2(data):
    goal = 2020
    for i, n1 in enumerate(data):
        for j, n2 in enumerate(data[i:]):
            for n3 in data[j:]:
                if n1 + n2 + n3 == goal:
                    return n1 * n2 * n3


def part2_cleaner_faster(data, goal=2020):
    for i, n1 in enumerate(data):
        new_goal = goal - n1
        ans = part1_faster(data[i+1:], goal=new_goal)
        if ans:
            return ans + (n1,)


def part2_faster(data):
    goal = 2020
    s = set(data)
    for i, n1 in enumerate(data):
        new_goal = goal - n1
        for n2 in data[i:]:
            if new_goal - n2 in s:
                return n1 * n2 * (new_goal - n2)


def main():
    a1 = part1(data)
    print(a1)

    a1 = part1_faster(data)
    print(a1, math.prod(a1))

    a2 = part2(data)
    print(a2)

    a2 = part2_cleaner_faster(data)
    print(a2, math.prod(a2))

    a2 = part2_faster(data)
    print(a2)


if __name__ == '__main__':
    input_file = 'input1.txt'
    data = load_data()
    main()

    t = timeit.Timer('part2_faster(data)', globals=globals())
    n = 10000
    print(sum(t.repeat(repeat=n, number=1)) / n)
