import re
from typing import List, Tuple


def load_data(filename):
    with open(filename, 'r') as f:
        return f.read().strip().split('\n\n')


class Board:
    def __init__(self, numbers: List[int], size=5, ):
        self.rows = [Row(idx=idx, numbers=numbers[idx * size: (idx + 1) * size]) for idx in range(size)]
        self.cols = [Col(idx=idx, numbers=numbers[idx:: size]) for idx in range(size)]

    def __str__(self):
        return ' '.join(map(str, self.rows)) + '\n' + ' '.join(map(str, self.cols))


class Row:
    def __init__(self, idx: int, numbers: List[int]):
        self.idx = idx
        self.numbers = set(numbers)

    def __str__(self):
        return f'{self.idx=}:' + ' '.join(map(str, self.numbers))


class Col(Row):
    def __init__(self, idx: int, numbers: List[int]):
        super().__init__(idx, numbers)


def part1():
    boards_copy = boards.copy()
    for n in random_numbers:
        for board in boards_copy:
            for row in board.rows:
                if n in row.numbers:
                    row.numbers.remove(n)
                    if len(row.numbers) == 0:
                        return n * sum([sum(r.numbers) for r in board.rows])

            for col in board.cols:
                if n in col.numbers:
                    col.numbers.remove(n)
                    if len(col.numbers) == 0:
                        return n * sum([sum(c.numbers) for c in board.cols])


def solve_board(board: Board):
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


def part2():
    boards_copy = boards.copy()
    solved_boards = sorted([solve_board(b) for b in boards_copy])
    return solved_boards[-1][1]


if __name__ == '__main__':
    input_file = 'day4.txt'
    data = load_data(input_file)

    random_numbers = list(map(int, data.pop(0).split(',')))

    boards = list()
    for item in data:
        board_numbers = list(map(int, re.split(r'[\s\\n]+', item.strip())))
        new_board = Board(board_numbers)
        boards.append(new_board)
    # print(*map(str, boards))

    print(part1())

    print(part2())
