import re
from copy import deepcopy
from typing import List


def load_data(filename):
    with open(filename, 'r') as f:
        pieces = f.read().strip().split('\n\n')

        # First item are the random numbers
        random_numbers = list(map(int, pieces.pop(0).split(',')))

        # All remaining items are the boards
        board_numbers_list = list()
        for item in pieces:
            # split item (a board) into numbers by splitting on whitespace and enters
            new_board_numbers = list(map(int, re.split(r'[\s\\n]+', item.strip())))
            board_numbers_list.append(new_board_numbers)
        return random_numbers, board_numbers_list


class Board:
    def __init__(self, numbers: List[int], size=5):
        self.rows = [Line(idx=idx, numbers=numbers[idx * size: (idx + 1) * size]) for idx in range(size)]
        self.cols = [Line(idx=idx, numbers=numbers[idx:: size]) for idx in range(size)]

    def __str__(self):
        return ' '.join(map(str, self.rows)) + '\n' + ' '.join(map(str, self.cols))


class Line:
    """A row or a column of a board."""
    def __init__(self, idx: int, numbers: List[int]):
        self.idx = idx
        self.numbers = set(numbers)

    def __str__(self):
        return f'{self.idx=}:' + ' '.join(map(str, self.numbers))


def solve_board(board: Board):
    """Determine:
     - how many turns needed to solve a board (i.e. bingo)
     - score: number that solves the board multiplied by remaining numbers."""
    for i, n in enumerate(random_numbers):
        for row in board.rows:
            if n in row.numbers:
                row.numbers.remove(n)
                if len(row.numbers) == 0:
                    return i, n * sum([sum(r.numbers) for r in board.rows])

        for col in board.cols:
            if n in col.numbers:
                col.numbers.remove(n)
                if len(col.numbers) == 0:
                    return i, n * sum([sum(c.numbers) for c in board.cols])


if __name__ == '__main__':
    input_file = 'day4.txt'
    random_numbers, board_numbers_list = load_data(input_file)

    # Create boards from board_numbers_list.
    boards = [Board(numbers=board_numbers) for board_numbers in board_numbers_list]

    # Solve boards, sort by number of turns needed to solve.
    solved_boards = sorted([solve_board(b) for b in deepcopy(boards)])

    # Return the score of board that was solved _first_.
    print(f'Part 1: {solved_boards[0][1]}')

    # Return the score of board that was solved _last_.
    print(f'Part 2: {solved_boards[-1][1]}')
