from collections import Counter


ORDER = "23456789TJQKA"
ORDER_P2 = "J23456789TQKA"


def get_type(hand, part2=False):
    """Return a number to represent the strength of the hand

    50 Five of a kind, where all five cards have the same label: AAAAA
    41 Four of a kind, where four cards have the same label and one card has a different label: AA8AA
    32 Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
    30 Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
    22 Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
    21 One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
    11 High card, where all cards' labels are distinct: 23456
    """
    c = Counter(hand)

    # adjust counts if hand contains a joker (J)
    # add counts of J to the card which occurs most frequently
    # if 5 J's, then don't adjust
    if part2 and "J" in c and len(c) > 1:
        j_count = c.pop("J")
        max_card = max(c, key=c.get)
        c[max_card] += j_count

    if 5 in c.values():
        return 50
    elif 4 in c.values():
        return 41
    elif 3 in c.values() and 2 in c.values():
        return 32
    elif 3 in c.values():
        return 30
    elif len(c) == 3:
        return 22
    elif len(c) == 4:
        return 21
    elif len(c) == 5:
        return 11

    raise ValueError("Invalid hand")


def greater_than(hand1, hand2, part2=False):
    """Is hand1 greater than hand2?"""
    hand1_type = get_type(hand1, part2)
    hand2_type = get_type(hand2, part2)
    if hand1 == hand2:
        return False

    order = ORDER_P2 if part2 else ORDER

    if hand1_type > hand2_type:
        return True
    elif hand1_type < hand2_type:
        return False
    elif hand1_type == hand2_type:
        for c1, c2 in zip(hand1, hand2):
            if order.index(c1) > order.index(c2):
                return True
            elif order.index(c1) < order.index(c2):
                return False
        raise ValueError("Shouldn't be able to get here.")


def part1(content, part2=False):
    lines = list(map(str.split, content.strip().split("\n")))
    ans = 0
    for hand1, bid in lines:
        rank = 1
        for hand2, _ in lines:
            if greater_than(hand1, hand2, part2):
                rank += 1
        ans += rank * int(bid)
    return ans


if __name__ == "__main__":
    SAMPLE = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""

    assert part1(SAMPLE) == 6440

    with open("day7.txt") as f:
        CONTENT = f.read()

    print(part1(CONTENT))

    assert part1(SAMPLE, part2=True) == 5905

    print(part1(CONTENT, part2=True))
