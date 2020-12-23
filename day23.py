def load_data():
    with open(input_file, 'r') as f:
        data = f.read().strip()
    return data


def part1():
    current_cup_idx = 0

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
    pass


def main():
    a1 = part1()
    print(a1)

    a2 = part2()
    print(a2)


if __name__ == '__main__':
    input_file = 'input23.txt'
    data = load_data()
    main()
