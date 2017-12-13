file = "C:\\Users\\Admin\\Desktop\\Work\\Learning\\Advent\\day6\\input.txt"
handle = open(file, 'r')

for line in handle:
    svals = line.split()

state = list()
for s in svals:
    state.append(int(s))

print("Initial state: \n", state)

run = 1
state_hash = list()
solved = False
while not solved:
    # find the maximum
    state_max = max(state)
    index_max = state.index(state_max)

    # redistribute
    pos = index_max
    state[pos] = 0
    while state_max > 0:
        pos += 1
        state[pos % 16] += 1
        state_max -= 1

    # create hash of state
    state_string = ''
    for s in state:
        state_string = state_string + str(s) + 'a'
    new_hash = hash(state_string)

    # check if hash already exists
    if new_hash in state_hash:
        solved = True
        print("Solved \nEnd state: \n", state, "\nAnswer:", run)
    else:
        state_hash.append(new_hash)

    run += 1
