def load_data():
    with open(input_file, 'r') as f:
        data = f.read().strip()
    return data


def part1():
    cups = list(map(int, data))
    current_label = cups[0]
    for round_ in range(100):
        current_cup_idx = cups.index(current_label)
        cups = cups[current_cup_idx:] + cups[:current_cup_idx]
        current_cup_idx = cups.index(current_label)

        pick_up = list()
        while len(pick_up) < 3:
            add = cups.pop((current_cup_idx+1) % len(cups))
            pick_up.append(add)

        destination_label = current_label - 1
        while destination_label not in cups:
            if destination_label == 0:
                destination_label = 9
            else:
                destination_label -= 1
        destination_idx = cups.index(destination_label)

        new_index = current_cup_idx + 1
        if new_index >= 6:
            new_index = 0
        current_label = cups[new_index]

        cups = cups[:destination_idx + 1] + pick_up + cups[destination_idx + 1:]

    one_idx = cups.index(1)
    ans = cups[one_idx+1:] + cups[:one_idx]
    return ''.join(map(str, ans))


def part2():
    cups = list(map(int, data))
    cups += list(range(10, int(1e6)+1))
    circle = dict(zip(cups, cups[1:] + cups[:1]))
    # print(circle)
    current_label = cups[-1]
    # rounds = 100
    rounds = int(1e7)
    for round_ in range(rounds):
        if round_ % 1000000 == 0:
            print(round_)

        current_label = circle[current_label]

        pick_up = list()
        tmp_label = current_label
        for _ in range(3):
            add = circle[tmp_label]
            tmp_label = add
            pick_up.append(add)
        # print(pick_up)
        circle[current_label] = circle[tmp_label]

        destination_label = current_label - 1
        while destination_label in pick_up or destination_label < 1:
            destination_label -= 1
            if destination_label < 1:
                destination_label = max(cups)

        # print(destination_label)

        circle[destination_label], circle[pick_up[-1]] = pick_up[0], circle[destination_label]

        new_current_label = circle[current_label]
        # print('new', new_current_label)
        # print(circle)

    # next_ = 1
    # for _ in range(8):
    #     next_ = circle[next_]
    #     # print(next_, end='')

    ans = 1
    next_ = 1
    for _ in range(2):
        next_ = circle[next_]
        ans *= next_
    return ans


def main():
    a1 = part1()
    print(a1)

    a2 = part2()
    print(a2)


if __name__ == '__main__':
    input_file = 'input23.txt'
    data = load_data()
    main()
