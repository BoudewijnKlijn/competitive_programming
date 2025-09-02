from typing import List


class Solution:
    def gameOfLife(self, board: List[List[int]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        """
        R, C = len(board), len(board[0])
        zeros = set()
        ones = set()
        for r in range(R):
            for c in range(C):
                count = 0
                for dr in range(-1, 2):
                    for dc in range(-1, 2):
                        rr = r + dr
                        cc = c + dc
                        if not dr and not dc:
                            continue
                        if 0 <= rr < R and 0 <= cc < C and board[rr][cc] == 1:
                            count += 1
                if board[r][c] and count < 2:
                    zeros.add((r, c))
                elif board[r][c] and count > 3:
                    zeros.add((r, c))
                elif board[r][c]:
                    ones.add((r, c))
                elif not board[r][c] and count == 3:
                    ones.add((r, c))
                else:
                    zeros.add((r, c))
        for r in range(R):
            for c in range(C):
                if (r, c) in ones:
                    board[r][c] = 1
                else:
                    board[r][c] = 0
        return board


if __name__ == "__main__":
    import os

    from timing import timing

    PROBLEM = "0289"
    data_file = os.path.join(os.path.dirname(__file__), f"leetcode_{PROBLEM}_data.txt")

    # # generate testcases
    # import sys

    # sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    # from generic.helper import InputInteger, InputList, generate_testcases

    # arr1 = InputList(n_min_max=(2, 100_000), val_min_max=(0, 10_000))
    # int1 = InputInteger(val_min_max=(0, 10_000))
    # vars = generate_testcases(structure=(arr1,), n=1, data_file=data_file, solver=None)

    timing(
        solution=Solution(),
        funcs=["gameOfLife"],
        data_file=data_file,
        exclude_data_lines=None,
        check_result=True,
    )
