import re
from dataclasses import dataclass
from itertools import cycle
from typing import Tuple
from collections import Counter
from copy import deepcopy
import itertools


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
    n_turns: int = 0

    def move(self, throw):
        self.position += throw
        while self.position > 10:
            self.position -= 10

    def increase_score(self):
        self.score += self.position
        self.n_turns += 1

    def __eq__(self, other):
        return self.position == other.position and self.score == other.score and self.n_turns == other.n_turns

    def __hash__(self):
        return hash((self.id, self.position, self.score, self.n_turns))


class Dice:
    def __init__(self):
        self.rolls = cycle(range(1, 100 + 1))
        self.n_rolls = 0

    def roll(self):
        self.n_rolls += 1
        return next(self.rolls)


DIRAC_SUM_THROWS = Counter(map(sum, itertools.product([1, 2, 3], repeat=3)))


def play_game():
    players = [Player(i, p) for i, p in enumerate(data)]
    dice = Dice()
    while True:
        for player in players:
            sum_throws = sum(dice.roll() for _ in range(3))
            player.move(sum_throws)
            player.increase_score()
            if player.score >= 1000:
                return min(p.score for p in players) * dice.n_rolls


def determine_turns_to_end_game(start):
    turn_counter = Counter()
    state_counts = Counter([start])
    while True:
        new_state = False
        new_state_counts = Counter()
        for player_state, count in state_counts.items():
            if player_state.score >= 21:
                turn_counter += Counter({player_state.n_turns: count})
                continue
            new_state = True
            for sum_throws, n_possible_ways_to_throw_sum in DIRAC_SUM_THROWS.items():
                new_state = deepcopy(player_state)
                new_state.move(sum_throws)
                new_state.increase_score()
                new_state_counts += Counter({new_state: count * n_possible_ways_to_throw_sum})
        state_counts = deepcopy(new_state_counts)

        if not new_state:
            return turn_counter


def do_turn(state_counts):
    """Should only receive states that are not finished yet."""
    new_state_counts = Counter()
    for player_state, count in state_counts.items():
        for sum_throws, n_possible_ways_to_throw_sum in DIRAC_SUM_THROWS.items():
            new_state = deepcopy(player_state)
            new_state.move(sum_throws)
            new_state.increase_score()
            new_state_counts += Counter({new_state: count * n_possible_ways_to_throw_sum})
    return new_state_counts


def part2():
    """For both players, run every possible game scenario, and stop them when they reach 21. Then compare the turns it
    took to get to 21. If turns tie, player 1 wins. Use counter to combine game and avoid explosion of number of games.
    """
    players = [Player(i, p) for i, p in enumerate(data)]
    unfinished_states_p1 = Counter([players[0]])
    unfinished_states_p2 = Counter([players[1]])
    game_wins = Counter({'p1': 0, 'p2': 0})
    while unfinished_states_p1 and unfinished_states_p2:
        state_counts_p1 = do_turn(unfinished_states_p1)
        unfinished_states_p1 = Counter()
        for player_state, count in state_counts_p1.items():
            if player_state.score >= 21:
                game_wins['p1'] += sum(unfinished_states_p2.values()) * count
                continue
            unfinished_states_p1 += Counter({player_state: count})

        state_counts_p2 = do_turn(unfinished_states_p2)

        # Simplify state_counts_p1 and state_counts_p2.
        # If player reached 21, remove those states and calculate how many resulted in a win.
        # Since player 1 is first, player 1 wins versus all states that have equal or more turns. Remove that number of
        # states from player 2. Same for player 2, except player 2 needs strictly fewer turns than player 1.

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
    assert play_game() == 739785
    assert part2() == 444356092776315

    # Actual data
    RAW = load_data('input.txt')
    data = parse_data(RAW)

    # Part 1
    print(f'Part 1: {play_game()}')

    # Part 2
    print(f'Part 2: {part2()}')
