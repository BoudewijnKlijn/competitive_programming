def calc(n, a, b, c):
    if a < c:
        return 'IMPOSSIBLE'
    if b < c:
        return 'IMPOSSIBLE'

    visible_only_a = a - c
    visible_only_b = b - c
    visible_both = c
    leftover = max(0, n - visible_only_a - visible_only_b - visible_both)

    if visible_only_a + visible_only_b + visible_both + leftover > n:
        return 'IMPOSSIBLE'

    if visible_only_b > 0:
        answer = [2] * visible_only_a + [n] * visible_both + [1] * leftover + [2] * visible_only_b
    elif visible_only_a > 0:
        answer = [2] * visible_only_a + [1] * leftover + [n] * visible_both
    elif visible_both >= 2:
        answer = [n] * 1 + [1] * leftover + [n] * (visible_both - 1)
    elif visible_both == 1 and leftover == 0:
        answer = [n] * visible_both
    else:
        return 'IMPOSSIBLE'

    return ' '.join(map(str, answer))


def main():
    # file_test_cases = 'test2020e2.txt'
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
        n, a, b, c = (int(i) for i in input().split(' '))
        print("Case #{}: {}".format(case, calc(n, a, b, c)))


if __name__ == '__main__':
    main()
