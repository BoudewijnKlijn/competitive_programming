import timeit


def load_data():
    with open(input_file, 'r') as f:
        data = list(map(int, f.read().strip().split()))
    return data


def is_in_preamble(preamble, pos, goal):
    s = set(data[pos-preamble: pos])
    for n1 in s:
        if (n2 := goal - n1) in s and n2 != n1:
            return n1, n2


def part1():
    preamble = 25
    for i, n in enumerate(data):
        if i < preamble:
            continue
        if is_in_preamble(preamble, pos=i, goal=n) is None:
            return n, i


def part2(maxi, needle):
    for begin in range(maxi):
        for end in range(begin+3, maxi):
            if (sum_ := sum(data[begin: end])) > needle:
                break

            if needle == sum_:
                return min(data[begin: end]) + max(data[begin: end])


def part2_faster(needle):
    begin, end = 0, 2
    sum_ = sum(data[begin:end])
    while sum_ != needle:
        if sum_ < needle:
            sum_ += data[end]
            end += 1
        else:
            sum_ -= data[begin]
            begin += 1
    return min(data[begin:end]) + max(data[begin:end])


def main():
    a1, i = part1()
    print(f'{a1=}, {i=}')

    a2 = part2(maxi=i, needle=a1)
    print(a2)

    a2 = part2_faster(needle=a1)
    print(a2)


if __name__ == '__main__':
    input_file = 'input9.txt'
    data = load_data()
    main()

    t = timeit.Timer('part1()', globals=globals())
    n = 10000
    print(sum(t.repeat(repeat=n, number=1)) / n)

    t = timeit.Timer('part2(maxi=509, needle=27911108)', globals=globals())
    n = 100
    print(sum(t.repeat(repeat=n, number=1)) / n)

    t = timeit.Timer('part2_faster(needle=27911108)', globals=globals())
    n = 10000
    print(sum(t.repeat(repeat=n, number=1)) / n)
