def calc(a, n):
    if n == 2:
        return 2

    max_length = 2
    current_length = 2

    prev_diff = a[1] - a[0]
    prev = a[1]

    for ai in a[2:]:
        diff = ai - prev

        if prev_diff == diff:
            current_length += 1
        else:
            current_length = 2

        if current_length > max_length:
            max_length = current_length

        prev_diff = diff
        prev = ai

    return max_length


def main():
    # file_test_cases = 'test2020e1.txt'
    # with open(file_test_cases, 'r') as f:
    #     contents = f.read().strip().split('\n')
    #
    # def gen(lines):
    #     for line in lines:
    #         yield line
    # 
    # input = gen(contents).__next__

    t = int(input())
    for case in range(1, t + 1):
        n = int(input())
        a = [int(i) for i in input().split(' ')]
        print("Case #{}: {}".format(case, calc(a, n)))


if __name__ == '__main__':
    main()
