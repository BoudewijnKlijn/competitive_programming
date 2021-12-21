import re
from dataclasses import dataclass
from itertools import cycle
from typing import Tuple
from collections import Counter


def load_data(filename: str) -> str:
    with open(filename, 'r') as f:
        return f.read()


def parse_data(raw_data: str) -> Tuple[int, int]:
    pattern = r'starting position: (\d+)'
    return tuple(map(int, re.findall(pattern, raw_data)))


@dataclass
class Player:
    id: int
    position: int
    score: int = 0

    def move(self, throw):
        self.position += throw
        while self.position > 10:
            self.position -= 10

    def increase_score(self):
        self.score += self.position

    def __eq__(self, other):
        return self.id == other.id and self.position == other.position and self.score == other.score

    def __hash__(self):
        return hash((self.id, self.position, self.score))


class Dice:
    def __init__(self):
        self.rolls = cycle(range(1, 100 + 1))
        self.turns = 0

    def roll(self):
        self.turns += 1
        return next(self.rolls)


def play_game():
    players = [Player(i, p) for i, p in enumerate(data)]
    dice = Dice()
    while True:
        for player in players:
            sum_throws = sum(dice.roll() for _ in range(3))
            player.move(sum_throws)
            player.increase_score()
            if player.score >= 1000:
                return min(p.score for p in players) * dice.turns


def part2():
    """For both players, run every possible game scenario, and stop them when they reach 21. Then compare the turns it
    took to get to 21. If turns tie, player 1 wins. Use counter to combine game and avoid explosion of number of games.
    """
    players = [Player(i, p) for i, p in enumerate(data)]
    player1_counts = Counter([players[0]])
    player2_counts = Counter([players[1]])

    for player in players:
        # one turn creates three universes
        p = [Player(0, data[0]) for _ in range(3)]
        a = Counter(p)
        print(a)




if __name__ == '__main__':
    # Sample data
    RAW = """Player 1 starting position: 4
Player 2 starting position: 8"""
    data = parse_data(RAW)

    # Assert solution is correct
    assert play_game() == 739785

    # Actual data
    RAW = load_data('input.txt')
    data = parse_data(RAW)

    # Part 1
    print(f'Part 1: {play_game()}')

    # Part 2
    print(f'Part 2: {part2()}')
