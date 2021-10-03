import numpy as np

matrix = np.zeros((401, 401))
input = 325489

row = 200
col = 200
value = 1
matrix[row, col] = value

# directions: 0: down, 1: right, 2: up, 3: left

direction = 1
side_length_completed = 0
side_length = 1
steps_taken = 0

while value < input:

    if steps_taken < side_length:
        pass
    else:
        # change direction
        direction = (direction + 1) % 4
        side_length_completed += 1
        steps_taken = 0

        if side_length_completed == 2:
            side_length += 1
            side_length_completed = 0

    steps_taken += 1

    if direction == 0:
        row += 1
    elif direction == 1:
        col += 1
    elif direction == 2:
        row -= 1
    else:
        col -= 1

    value = np.sum(matrix[row-1: row+2, col-1: col+2])
    matrix[row, col] = value

print(value)
