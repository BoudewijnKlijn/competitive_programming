def calc(a, n):
    print(a, n)


def main():
    file_test_cases = 'test2020e1.txt'
    with open(file_test_cases, 'r') as f:
        contents = f.read().strip().split('\n')

    def gen(lines):
        for line in lines:
            yield line

    input = gen(contents).__next__

    t = int(input())
    for case in range(1, t + 1):
        n = int(input())
        a = [int(i) for i in input().split(' ')]
        print("Case #{}: {}".format(case, calc(a, n)))


if __name__ == '__main__':
    main()

