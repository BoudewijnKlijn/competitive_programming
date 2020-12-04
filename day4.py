import timeit


def load_data():
    with open(input_file, 'r') as f:
        data = [x.split() for x in f.read().strip().split('\n\n')]

    passports = list()
    for passport in data:
        d = dict()
        for code in passport:
            k, v = code.split(':')
            d[k] = v
        passports.append(d)
    # print(passports)
    return passports


def part1(data):
    keys = ['byr','iyr','eyr','hgt','hcl','ecl','pid','cid']
    valids = 0
    for passport in data:
        print(passport)
        fields = 0
        for key in keys:
            value = passport.get(key)
            if value or key == 'cid':
                fields += 1
        if fields == 8:
            valids += 1

    return valids

        # print(len(passport))
    pass


def part2(data):
    pass


def main():
    a1 = part1(data)
    print(a1)

    a2 = part2(data)
    print(a2)


if __name__ == '__main__':
    input_file = 'input4.txt'
    data = load_data()
    main()

    # t = timeit.Timer('par1(data)', globals=globals())
    # n = 10000
    # print(sum(t.repeat(repeat=n, number=1)) / n)
