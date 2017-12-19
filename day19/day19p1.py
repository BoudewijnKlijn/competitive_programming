def pos_to_rc(position):
    row = position // cols
    col = position % cols
    return row, col


def rc_to_pos(tup):
    row, col = tup
    return row * cols + col


def move(position, direction):
    row, col = pos_to_rc(position)
    if direction == 'down':
        row += 1
    elif direction == 'up':
        row -= 1
    elif direction == 'left':
        col -= 1
    else:
        col += 1
    if row < 0 or row >= rows or col < 0 or col >= cols:
        return False
    return rc_to_pos((row, col))


file = 'C:\\Users\\Admin\\Desktop\\Work\\Learning\\Advent\\day19\\input.txt'
handle = open(file, 'r')
contents = handle.read()

# see what characters are in the input
chars = []
for char in contents:
    if char not in chars:
        chars.append(char)

# number of chars
total_chars = len(contents)

# first newline at pos 201, so 201 informative characters per line + newline at end = 202
chars_per_line = contents.find("\n") + 1
cols = chars_per_line

# number of rows
rows = int(total_chars / chars_per_line)

# start position
col = contents.find("|")
row = 0
position = rc_to_pos((row, col))
char = contents[position]
direction = 'down'
directions = []
positions = [(row, col)]
all_directions = ['down', 'up', 'left', 'right']
counter_directions = {'down': 'up', 'up': 'down', 'left': 'right', 'right': 'left'}
route = [char]

while 0 <= row < rows and 0 <= col < cols:

    # make move to new position and store it
    position = move(position, direction)
    positions.append(pos_to_rc(position))
    directions.append(direction)
    route.append(contents[position])

    if move(position, direction) and contents[move(position, direction)] != ' ':
        # continue with same direction if it is valid
        continue
    else:
        # determine new valid direction
        possible_directions = all_directions.copy()
        possible_directions.remove(direction)
        possible_directions.remove(counter_directions[directions[-1]])
        if move(position, possible_directions[0]) and contents[move(position, possible_directions[0])] != ' ':
            direction = possible_directions[0]
            continue
        elif move(position, possible_directions[1]) and contents[move(position, possible_directions[1])] != ' ':
            direction = possible_directions[1]
            continue
        else:
            break

allowed_chars = ['A', 'X', 'Z', 'I', 'U', 'S', 'B', 'Y', 'W']
answer = ''.join([char for char in route if char in allowed_chars])
print("Answer part 1:", answer)

print("Answer part 2:", len(route))
