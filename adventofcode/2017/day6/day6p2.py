def create_state_hash(state):
    state_string = ''
    for bank_val in state:
        state_string = state_string + str(bank_val) + 'a'
    return hash(state_string)


file = "C:\\Users\\Admin\\Desktop\\Work\\Learning\\Advent\\day6\\input.txt"
handle = open(file, 'r')

for line in handle:
    svals = line.split()

state = list()
for s in svals:
    state.append(int(s))

# use end state of part 1 as initial state
state = [1, 0, 14, 14, 12, 12, 10, 10, 8, 8, 6, 6, 4, 3, 2, 1]

print("Initial state: \n", state)

run = 1
state_hash = [create_state_hash(state)]
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
    new_hash = create_state_hash(state)

    # check if hash already exists
    if new_hash in state_hash:
        solved = True
        print("Solved \nEnd state: \n", state, "\nAnswer:", run)
    else:
        state_hash.append(new_hash)

    run += 1
