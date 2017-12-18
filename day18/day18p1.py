def retrieve(sval):
    try:
        ival = int(sval)
    except:
        ival = registers[sval]
    return ival


def execute_line(line_id):
    global play

    line = line_by_line[line_id]
    operation = line.split()[0]
    register = line.split()[1]
    ival1 = retrieve(register)

    try:
        ival2 = retrieve(line.split()[2])
    except:
        pass

    if operation == 'set':
        registers[register] = ival2

    elif operation == 'mul':
        registers[register] *= ival2

    elif operation == 'jgz' and ival1 > 0:
        line_id += ival2
        return line_id

    elif operation == 'add':
        registers[register] += ival2

    elif operation == 'mod':
        registers[register] %= ival2

    elif operation == 'snd':
        play = ival1

    elif operation == 'rcv' and ival1 != 0:
        print("Answer part 1:", play)
        return False

    return line_id+1


file = 'C:\\Users\\Admin\\Desktop\\Work\\Learning\\Advent\\day18\\input.txt'
# file = 'C:\\Users\\Admin\\Desktop\\Work\\Learning\\Advent\\day18\\test_input.txt'
handle = open(file, 'r')
contents = handle.read()

line_by_line = contents.strip().split('\n')
registers = dict()

# initialize all registers with 0
for line in line_by_line:
    register = line.split()[1]
    if register not in registers.keys() and not register.isdigit():
        registers[register] = 0

play = None
line_id = 0
while 0 <= line_id < len(line_by_line):
    # print(line_id, line_by_line[line_id])
    # print(registers)
    line_id = execute_line(line_id)
    # print(registers)
    # print("")
    # input("enter")
    if not line_id:
        break
