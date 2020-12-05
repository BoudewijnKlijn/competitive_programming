import timeit
import re


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
    return passports


def is_valid_p2(key, value):
    if key == 'byr':
        try:
            i = int(value)
            if 1920 <= i <= 2002:
                return True
        except:
            return False

    if key == 'iyr':
        try:
            i = int(value)
            if 2010 <= i <= 2020:
                return True
        except:
            return False

    if key == 'eyr':
        try:
            i = int(value)
            if 2020 <= i <= 2030:
                return True
        except:
            return False

    if key == 'hgt':
        if value[-2:] == 'in':
            try:
                i = int(value[:-2])
                if 59 <= i <= 76:
                    return True
            except:
                return False
        elif value[-2:] == 'cm':
            try:
                i = int(value[:-2])
                if 150 <= i <= 193:
                    return True
            except:
                return False

    if key == 'hcl':
        pattern = '#[a-f0-9]{6}'
        g = re.findall(pattern, value)
        if len(g) == 1:
            return True

    if key == 'ecl':
        if value in ['amb','blu','brn','gry','grn','hzl','oth']:
            return True

    if key == 'pid':
        pattern = '[0-9]{9}'
        g = re.findall(pattern, value)
        if len(g) == 1 and len(value) == 9:
            return True


def part1(data):
    keys = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']  # 'cid'

    valids = 0
    for passport in data:
        if all([k in passport.keys() for k in keys]):
        # if (n := len((k := passport.keys()))) == 8 or (n == 7 and 'cid' not in k):
            valids += 1
    return valids


def part2(data):
    valids = 0
    for passport in data:
        if (n := len((k := passport.keys()))) == 8 or (n == 7 and 'cid' not in k):
            fields = 0
            for key, value in passport.items():
                if is_valid_p2(key, value):
                    fields += 1
            if fields in [7, 8]:
                valids += 1
    return valids


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
