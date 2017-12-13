file = 'input.txt'
path = 'C:\\Users\\Admin\\Desktop\\Work\\Learning\\Advent\\day5\\'
handle = open(path+file, 'r')

# store input in a list
maze = list()
for line in handle:
    sval = line.rsplit()
    ival = int(sval[0])
    maze.append(ival)

# step through maze while new position is between 0 and length of maze
new_pos = 0
steps = 0
while new_pos in range(len(maze)):
    pos = new_pos
    new_pos += maze[pos]

    # added for part 2
    if maze[pos] >= 3:
        maze[pos] -= 1
    else:
        maze[pos] += 1
    steps += 1

print(steps)
