import re
from collections import Counter
from copy import deepcopy
from dataclasses import dataclass
from itertools import cycle, product
from typing import Tuple


def load_data(filename: str) -> str:
    with open(filename, 'r') as f:
        return f.read()


def parse_data(raw_data: str) -> Tuple[int, int]:
    pattern = r'starting position: (\d+)'
    return tuple(map(int, re.findall(pattern, raw_data)))


@dataclass
class Player:
    position: int
    score: int = 0

    def move(self, throw):
        self.position += throw
        while self.position > 10:
            self.position -= 10

    def increase_score(self):
        self.score += self.position

    def __eq__(self, other):
        return self.position == other.position and self.score == other.score

    def __hash__(self):
        return hash((self.position, self.score))


class Dice:
    def __init__(self):
        self.rolls = cycle(range(1, 101))
        self.n_rolls = 0

    def roll(self):
        self.n_rolls += 1
        return next(self.rolls)


def part1():
    players = [Player(p) for p in data]
    dice = Dice()
    while True:
        for player in players:
            sum_throws = sum(dice.roll() for _ in range(3))
            player.move(sum_throws)
            player.increase_score()
            if player.score >= 1000:
                return min(p.score for p in players) * dice.n_rolls


DIRAC_SUM_THROWS = Counter(map(sum, product([1, 2, 3], repeat=3)))


def do_turn(state_counts):
    """Execute a turn for unfinished states."""
    new_state_counts = Counter()
    for player_state, count in state_counts.items():
        for sum_throws, n_possible_ways_to_throw_sum in DIRAC_SUM_THROWS.items():
            new_state = deepcopy(player_state)
            new_state.move(sum_throws)
            new_state.increase_score()
            new_state_counts += Counter({new_state: count * n_possible_ways_to_throw_sum})
    return new_state_counts


def part2():
    """Aggregate states to avoid blowing up. States are determined by position and score. If a state is finished, it
    wins from all unfinished states. Continue until all games are finished."""
    game_wins = Counter({'p1': 0, 'p2': 0})
    players = [Player(p) for p in data]

    unfinished_states_p1 = Counter([players[0]])
    unfinished_states_p2 = Counter([players[1]])
    while unfinished_states_p1 and unfinished_states_p2:
        # Execute player 1 turn.
        state_counts_p1 = do_turn(unfinished_states_p1)

        # Keep unfinished states. Use finished states to count wins.
        unfinished_states_p1 = Counter()
        for player_state, count in state_counts_p1.items():
            if player_state.score >= 21:
                game_wins['p1'] += sum(unfinished_states_p2.values()) * count
                continue
            unfinished_states_p1 += Counter({player_state: count})

        # Execute player 2 turn.
        state_counts_p2 = do_turn(unfinished_states_p2)

        # Keep unfinished states. Use finished states to count wins.
        unfinished_states_p2 = Counter()
        for player_state, count in state_counts_p2.items():
            if player_state.score >= 21:
                game_wins['p2'] += sum(unfinished_states_p1.values()) * count
                continue
            unfinished_states_p2 += Counter({player_state: count})

    return max(game_wins.values())


if __name__ == '__main__':
    # Sample data
    RAW = """Player 1 starting position: 4
Player 2 starting position: 8"""
    data = parse_data(RAW)

    # Assert solution is correct
    assert part1() == 739785
    assert part2() == 444356092776315

    # Actual data
    RAW = load_data('day21.txt')
    data = parse_data(RAW)

    # Part 1
    print(f'Part 1: {part1()}')

    # Part 2
    print(f'Part 2: {part2()}')
