from dataclasses import dataclass
import re
from typing import List, Tuple, Union
from collections import defaultdict
from itertools import cycle
from collections import Counter
import numpy as np


def load_data(filename: str) -> str:
    with open(filename, 'r') as f:
        return f.read()


def parse_data(raw_data: str) -> List[int]:
    pattern = r'starting position: (\d+)'
    starting_positions = tuple(map(int, re.findall(pattern, raw_data)))
    return starting_positions


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


class Dice:
    def __init__(self):
        self.rolls = cycle(range(1, 100 + 1))
        self.turns = 0

    def roll(self):
        self.turns += 1
        return next(self.rolls)


def play_game():
    print(data)
    players = [Player(i, p) for i, p in enumerate(data)]
    stop_game = False
    dice = Dice()
    while not stop_game:
        for player in players:
            if stop_game:
                break
            sum_throws = sum(dice.roll() for _ in range(3))
            player.move(sum_throws)
            player.increase_score()
            if player.score >= 1000:
                stop_game = True
            print(player)

    return min(p.score for p in players) * dice.turns


if __name__ == '__main__':
    # Sample data
    RAW = """Player 1 starting position: 4
Player 2 starting position: 8"""
    data = parse_data(RAW)

    # Assert solution is correct

    # Actual data
    RAW = load_data('input.txt')
    data = parse_data(RAW)

    print(play_game())