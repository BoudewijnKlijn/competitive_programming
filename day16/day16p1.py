import time

file = 'C:\\Users\\Admin\\Desktop\\Work\\Learning\\Advent\\day16\\input.txt'
handle = open(file, 'r')
contents = handle.read().strip()

start = time.time()

programs = 'abcdefghijklmnop'
instructions = contents.split(',')
for instruction in instructions:
    if instruction[0] == 's':
        x = int(instruction[1:])
        programs = programs[-x:] + programs[:-x]
    elif instruction[0] == 'x':
        ab = instruction[1:].split('/')
        a = int(ab[0])
        b = int(ab[1])
        tmp = [char for char in programs]
        tmp[a], tmp[b] = tmp[b], tmp[a]
        programs = ''.join(tmp)
    elif instruction[0] == 'p':
        ab = instruction[1:].split('/')
        a = ab[0]
        b = ab[1]
        a_index = programs.index(a)
        b_index = programs.index(b)
        tmp = [char for char in programs]
        tmp[a_index], tmp[b_index] = tmp[b_index], tmp[a_index]
        programs = ''.join(tmp)

end = time.time()
print("Answer p1: %s. Took %0.4f seconds." % (programs, end-start))

