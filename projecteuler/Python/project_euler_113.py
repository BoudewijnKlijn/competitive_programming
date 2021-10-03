# write out possibilities for places left and current digit. then it becomes clear what the relation is.
# a sort of pascal triangle

import numpy as np


def main():

    max_digits = 100

    # increasing
    matrix = np.zeros((max_digits, 9), dtype=np.int64)
    matrix[0, :] = 1

    for row in range(1, max_digits):
        for col in reversed(range(9)):
            matrix[row, col] = np.sum(matrix[row-1:row, col:])

    # decreasing
    matrixd = np.zeros((max_digits, 9), dtype=np.int64)
    matrixd[0, :] = 1

    for row in range(1, max_digits):
        for col in range(9):
            matrixd[row, col] = matrixd[row - 1:row, 0:col+1].sum() + 1

    increasing = matrix.sum()
    decreasing = matrixd.sum()
    double_counts = max_digits * 9  # all numbers with all the same digits
    non_bouncy = increasing + decreasing - double_counts

    # print(matrix)
    print(non_bouncy)


if __name__ == '__main__':
    main()
