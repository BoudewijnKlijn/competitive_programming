import timeit
import re


def load_data():
    with open(input_file, 'r') as f:
        data = f.read().strip().split('\n')
    return data


def parse_data():
    pass


def int_to_mask(num):
    return list(map(int, '{0:0=36b}'.format(int(num))))


def combine_masks(value_mask, memory_mask):
    memory = int_to_mask(0)
    for i, (mm, vm) in enumerate(zip(memory_mask, value_mask)):
        if mm != 'X':
            memory[i] = int(mm)
        else:
            memory[i] = int(vm)
    return memory


def combine_masks_p2(value_mask, memory_mask):
    memory = list(map(str, int_to_mask(0)))
    for i, (mm, vm) in enumerate(zip(memory_mask, value_mask)):
        if mm == '0':
            memory[i] = str(vm)
        elif mm in '1X':
            memory[i] = mm
        else:
            NotImplementedError()
    return memory


def part1():
    memory_dict = dict()
    for line in data:
        if 'mask' in line:
            memory_mask = line.split(' ')[-1]
        elif 'mem' in line:
            index_, value = re.findall(r'[\d]+', line)
            mem2 = int_to_mask(value)
            memory_dict[index_] = combine_masks(mem2, memory_mask)

    sum_ = 0
    for k, v in memory_dict.items():
        sum_ += int(''.join(map(str, v)), 2)
    return sum_


def part2():
    memory_dict = dict()
    for line in data:
        if 'mask' in line:
            memory_mask = line.split(' ')[-1]
        elif 'mem' in line:
            index_, value = re.findall(r'[\d]+', line)
            mem2 = int_to_mask(index_)
            base = combine_masks_p2(mem2, memory_mask)
            # print(base)
            xcount = memory_mask.count('X')
            # print(xcount)
            for replacement_run in range(2**xcount):
                # print(replacement_run)
                replacement_bits = int_to_mask(replacement_run)[::-1]
                # print(replacement_bits)
                trial = base.copy()

                for i, bit in enumerate(trial[::-1]):
                    if bit == 'X':
                        trial[-i-1] = str(replacement_bits.pop(0))
                index_ = int(''.join(trial), 2)
                # print(index_, value)
                memory_dict[index_] = int(value)
                # print('trial', trial)

    sum_ = 0
    for k, v in memory_dict.items():
        # print(k, strv)
        sum_ += v
    return sum_


def main():
    a1 = part1()
    print(a1)

    a2 = part2()
    print(a2)


if __name__ == '__main__':
    input_file = 'input14.txt'
    data = load_data()
    parsed = parse_data()
    main()

    # t = timeit.Timer('part1(p1=False)', globals=globals())
    # n = 100
    # print(sum(t.repeat(repeat=n, number=1)) / n)
