import timeit
import re
from functools import reduce


def load_data():
    with open(input_file, 'r') as f:
        data = f.read().strip()
    return data


def parse_data():
    player1, player2 = data.split('\n\n')
    player1_cards, player2_cards = list(), list()
    for i, (player1_card, player2_card) in enumerate(zip(player1.split('\n'), player2.split('\n'))):
        if i == 0:
            continue
        player1_cards.append(int(player1_card))
        player2_cards.append(int(player2_card))
    return player1_cards, player2_cards


def play_game():
    player1_cards, player2_cards = parsed
    round_ = 0
    while player1_cards and player2_cards:
        round_ += 1
        p1_card, p2_card = player1_cards.pop(0), player2_cards.pop(0)
        if p1_card > p2_card:
            player1_cards += [p1_card, p2_card]
        elif p2_card > p1_card:
            player2_cards += [p2_card, p1_card]
        else:
            raise NotImplementedError()
    return player1_cards, player2_cards, round_


def part1():
    player1_cards, player2_cards, ans = play_game()
    if len(player1_cards) > 0:
        ans = sum([i * c for i, c in enumerate(player1_cards[::-1], start=1)])
    else:
        ans = sum([i * c for i, c in enumerate(player2_cards[::-1], start=1)])

    print(ans)



def part2():
    pass


def main():
    a1 = part1()
    print(a1)

    a2 = part2()
    print(a2)


if __name__ == '__main__':
    input_file = 'input22.txt'
    data = load_data()
    parsed = parse_data()
    main()

    # t = timeit.Timer('part2_regex()', globals=globals())
    # n = 10
    # print(sum(t.repeat(repeat=n, number=1)) / n)
