import time


class Program(object):

    def __init__(self, pid):
        self.pid = pid
        self.registers = dict()
        self.registers['p'] = self.pid
        self.line_id = 0
        self.receive_list = []
        self.waiting_for_input = False
        self.send_counter = 0

        # initialize registers
        for line in line_by_line:
            register = line.split()[1]
            if register not in self.registers.keys() and not register.isdigit():
                self.registers[register] = 0

    def retrieve(self, sval):
        try:
            ival = int(sval)
        except:
            ival = self.registers[sval]
        return ival

    def execute_line(self, line_id):
        global play

        line = line_by_line[line_id]
        operation = line.split()[0]
        register = line.split()[1]
        ival1 = self.retrieve(register)

        try:
            ival2 = self.retrieve(line.split()[2])
        except:
            pass

        if operation == 'set':
            self.registers[register] = ival2

        elif operation == 'mul':
            self.registers[register] *= ival2

        elif operation == 'jgz' and ival1 > 0:
            self.line_id += ival2
            return self.line_id

        elif operation == 'add':
            self.registers[register] += ival2

        elif operation == 'mod':
            self.registers[register] %= ival2

        elif operation == 'snd':
            self.send_counter += 1
            if self.pid == 0:
                p1.receive_list.append(ival1)
                p1.waiting_for_input = False
            elif self.pid == 1:
                p0.receive_list.append(ival1)
                p0.waiting_for_input = False
            else:
                print("Error, pid shouldn't exist...")
                time.sleep(100)

        elif operation == 'rcv':
            if len(self.receive_list) > 0:
                self.registers[register] = self.receive_list[0]
                self.receive_list.pop(0)
            else:
                self.waiting_for_input = True
                return line_id

        return self.line_id + 1


file = 'C:\\Users\\Admin\\Desktop\\Work\\Learning\\Advent\\day18\\input.txt'
# file = 'C:\\Users\\Admin\\Desktop\\Work\\Learning\\Advent\\day18\\test_input.txt'
# file = 'C:\\Users\\Admin\\Desktop\\Work\\Learning\\Advent\\day18\\test_input_part2.txt'
handle = open(file, 'r')
contents = handle.read()

line_by_line = contents.strip().split('\n')

p0 = Program(0)
p1 = Program(1)
programs = [p0, p1]

while True:
    if not 0 <= p0.line_id < len(line_by_line) or not 0 <= p1.line_id < len(line_by_line):
        break
    elif all([program.waiting_for_input for program in programs]):
        break

    for program in programs:
        if not program.waiting_for_input:
            program.line_id = program.execute_line(program.line_id)

print("Answer part 2:", p1.send_counter)
