

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


def play_game(player1_cards, player2_cards):
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
    return len(player1_cards) > 0, player1_cards, player2_cards, round_


def play_game_v2(player1_cards, player2_cards):
    round_ = 0
    p1_previous, p2_previous = set(), set()
    while player1_cards and player2_cards:

        if (p1_hand := '_'.join(map(str, player1_cards))) in p1_previous:
            return True, None, None, None
        if (p2_hand := '_'.join(map(str, player2_cards))) in p2_previous:
            return True, None, None, None
        p1_previous.add(p1_hand)
        p2_previous.add(p2_hand)

        round_ += 1
        p1_card, p2_card = player1_cards.pop(0), player2_cards.pop(0)
        if p1_card <= len(player1_cards) and p2_card <= len(player2_cards):
            p1_wins, _, _, _ = play_game_v2(player1_cards.copy()[:p1_card], player2_cards.copy()[:p2_card])
            if p1_wins:
                player1_cards += [p1_card, p2_card]
            else:
                player2_cards += [p2_card, p1_card]
        elif p1_card > p2_card:
            player1_cards += [p1_card, p2_card]
        elif p2_card > p1_card:
            player2_cards += [p2_card, p1_card]
        else:
            raise NotImplementedError()

    return len(player1_cards) > 0, player1_cards, player2_cards, round_


def part1():
    player1_cards, player2_cards = parsed
    p1_wins, player1_cards, player2_cards, ans = play_game(player1_cards.copy(), player2_cards.copy())
    if p1_wins:
        ans = sum([i * c for i, c in enumerate(player1_cards[::-1], start=1)])
    else:
        ans = sum([i * c for i, c in enumerate(player2_cards[::-1], start=1)])
    return ans


def part2():
    player1_cards, player2_cards = parsed
    p1_wins, player1_cards, player2_cards, ans = play_game_v2(player1_cards.copy(), player2_cards.copy())
    if p1_wins:
        ans = sum([i * c for i, c in enumerate(player1_cards[::-1], start=1)])
    else:
        ans = sum([i * c for i, c in enumerate(player2_cards[::-1], start=1)])
    return ans


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
