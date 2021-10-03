# check if there is a repeating cycle. occurs every 60 runs. 10**9 % 60 = 40. answer is same as after 40 runs.
import time

file = 'C:\\Users\\Admin\\Desktop\\Work\\Learning\\Advent\\day16\\input.txt'
handle = open(file, 'r')
contents = handle.read().strip()

programs = 'abcdefghijklmnop'
programs = [char for char in programs]
instructions = contents.split(',')

start = time.time()

for run in range(40):

    if programs == [char for char in 'abcdefghijklmnop'] and run != 0:
        print(run)

    for instruction in instructions:
        if instruction[0] == 's':
            x = int(instruction[1:])
            programs = programs[-x:] + programs[:-x]
        elif instruction[0] == 'x':
            ab = instruction[1:].split('/')
            a = int(ab[0])
            b = int(ab[1])
            programs[a], programs[b] = programs[b], programs[a]
        elif instruction[0] == 'p':
            ab = instruction[1:].split('/')
            a = ab[0]
            b = ab[1]
            a_index = programs.index(a)
            b_index = programs.index(b)
            programs[a_index], programs[b_index] = programs[b_index], programs[a_index]

end = time.time()
print("Answer p2: %s. Took %0.4f seconds." % (''.join(programs), end-start))
