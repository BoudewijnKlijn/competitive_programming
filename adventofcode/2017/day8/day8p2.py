# file = 'C:\\Users\\Admin\\Desktop\\Work\\Learning\\Advent\\day8\\test.txt'
file = 'C:\\Users\\Admin\\Desktop\\Work\\Learning\\Advent\\day8\\input.txt'

# initialization of registers
handle = open(file, 'r')
registers = dict()
for line in handle:
    registers[line.split()[0]] = 0

# determine in- or decrement value
handle = open(file, 'r')
max_val = 0
for line in handle:
    words = line.split()
    subject = words[0]
    in_decrement = int(words[2]) if words[1] == 'inc' else -1 * int(words[2])
    key = words[4]
    condition = words[5]
    value = int(words[6])

    if key not in registers.keys():
        print("Not in register")
        break

    if condition == '>' and registers[key] > value:
        registers[subject] += in_decrement
    elif condition == '<' and registers[key] < value:
        registers[subject] += in_decrement
    elif condition == '==' and registers[key] == value:
        registers[subject] += in_decrement
    elif condition == '>=' and registers[key] >= value:
        registers[subject] += in_decrement
    elif condition == '<=' and registers[key] <= value:
        registers[subject] += in_decrement
    elif condition == '!=' and registers[key] != value:
        registers[subject] += in_decrement

    for k, v in registers.items():
        if v > max_val:
            max_val = v

print("Answer:", max_val)
