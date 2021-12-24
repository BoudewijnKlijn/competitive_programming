import re
from itertools import product
from typing import List
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from queue import PriorityQueue
from copy import deepcopy


def load_data(filename: str) -> str:
    with open(filename, 'r') as f:
        return f.read()


def parse_data(raw_data: str):
    commands = []
    for line in raw_data.splitlines():
        commands.append(line.split())
    return commands


class StringAlu:
    def __init__(self, commands: List[List[str]]):
        self.x = '0'
        self.y = '0'
        self.z = '0'
        self.w = '0'
        self.commands = commands
        self.inputs = [f'INP_' + str(i).zfill(2) for i in range(14)]

    def __repr__(self):
        return f'{self.x=}\n{self.y=}\n{self.z=}\n{self.w=}'

    @staticmethod
    def add(a, b):
        if a == '0':
            return b
        elif b == '0':
            return a
        return f'({a} + {b})'

    @staticmethod
    def mul(a, b):
        if a == '1':
            return b
        elif b == '1':
            return a
        elif a == '0':
            return '0'
        elif b == '0':
            return '0'
        return f'({a} * {b})'

    @staticmethod
    def div(a, b):
        if a == '0':
            return a
        if b == '1':
            return a
        elif b == '0':
            return 'ERROR'
        return f'({a} // {b})'

    @staticmethod
    def mod(a, b):
        if b == 1:
            return a
        return f'({a} % {b})'

    @staticmethod
    def eql(a, b):
        # equal is a bit more complex to evaluate if it contains an input. input can be between 1 and 9. we can try
        # all options and if they all yield the same value, then we return that
        base_out = f'({a} == {b})'
        # print('base', base_out)
        answers = list()
        pattern = re.compile(r'INP_\d{2}')
        inputs = list(set(pattern.findall(base_out)))
        if inputs:
            print(len(inputs))
            for substitutions in product(range(1, 10), repeat=len(inputs)):
                # print(substitutions)
                try:
                    adjusted = base_out
                    # loop over all inputs that need to be substituted
                    for sub_i, sub in enumerate(substitutions):
                        adjusted = adjusted.replace(inputs[sub_i], str(sub))
                    # all inputs are adjusted, now evaluate the expression
                    answer = eval(adjusted)
                except Exception as e:
                    print(e)
                    print(base_out, '\n', adjusted)
                    return base_out
                answers.append(answer)
            # print(answers)
            if all(answers):
                print(all(answers))
                return '1'
            elif not any(answers):
                print(all(answers))
                return '0'
            else:
                print('mix of true and false')
                print(answers)

        return f'({a} == {b})'

    def execute_commands(self):
        for j, cmd in enumerate(self.commands):
            print(f'{j}: {cmd}')
            instruction = cmd[0]
            var = cmd[1]
            if instruction == 'inp':
                value = self.inputs.pop(0)
                setattr(self, var, value)
            elif instruction in ['add', 'mul', 'mod', 'div', 'eql']:
                func = getattr(self, instruction)
                try:
                    value = int(cmd[2])
                except ValueError:
                    value = getattr(self, cmd[2])
                value = str(value)

                # evaluate the expression
                result = func(getattr(self, var), value)
                try:
                    tmp = eval(result)
                    if isinstance(tmp, int):
                        result = str(int(tmp))
                except:
                    pass
                setattr(self, var, result)
            else:
                raise ValueError(f"Unknown instruction {instruction}.")
            # print(self)
            # input()


class Alu:
    def __init__(self, commands: List[List[str]], inputs: List[int]):
        self.x = 0
        self.y = 0
        self.z = 0
        self.w = 0
        self.commands = commands
        self.command_i = 0
        self.inputs = inputs
        self.input_i = 0

    def __repr__(self):
        return f'{self.x=}\n{self.y=}\n{self.z=}\n{self.w=}'

    @staticmethod
    def add(a, b):
        return a + b

    @staticmethod
    def mul(a, b):
        return a * b

    @staticmethod
    def div(a, b):
        if b == 0:
            raise ValueError(f"{b} is zero")
        return int(a / b)  # using // does not truncate towards zero

    @staticmethod
    def mod(a, b):
        if a < 0:
            raise ValueError(f"{a} is negative")
        if b <= 0:
            raise ValueError(f"{b} is non-positive")
        return a % b

    @staticmethod
    def eql(a, b):
        return (a == b) * 1

    def execute_commands(self):
        while True:
            if self.command_i >= len(self.commands):
                if self.z == 0:
                    print(self)
                    exit(0)
                else:
                    return False
            cmd = self.commands[self.command_i]
            instruction = cmd[0]
            var = cmd[1]
            if instruction == 'inp':
                try:
                    value = self.inputs[self.input_i]
                except IndexError:
                    # decrease command index by 1 to start from there next time
                    self.command_i -= 1
                    return True
                self.input_i += 1
                assert 1 <= value <= 9, f"{value} is not in range"
                setattr(self, var, value)
            elif instruction in ['add', 'mul', 'mod', 'div', 'eql']:
                func = getattr(self, instruction)
                try:
                    value = int(cmd[2])
                except ValueError:
                    value = getattr(self, cmd[2])

                try:
                    setattr(self, var, func(getattr(self, var), value))
                except ValueError:
                    return False
            else:
                raise ValueError(f"Unknown instruction {instruction}.")

            # increase command index
            self.command_i += 1


def is_valid(fourteen_digit_number):
    alu = Alu(commands=commands, inputs=list(fourteen_digit_number))
    alu.execute_commands()
    valid = alu.z == 0
    if valid:
        print('input', fourteen_digit_number)
        print('z', alu.z)
    return valid


def gen_fourteen_digit_number(n: int = int(1e5)):
    # this is sorted and does not change output
    # return product(range(1, 10), repeat=14)

    # this is random, yields more insights
    return np.random.randint(1, 10, size=(n, 14))


def part1():
    max_valid_number = None
    start = 0
    for i, fourteen_digit_number in enumerate(iter(gen_fourteen_digit_number()), start=0):
        print(i, fourteen_digit_number)
        if i < start:
            continue
        if i % 1000 == 0:
            print(i)
        if is_valid(fourteen_digit_number):
            number = int(''.join(map(str, fourteen_digit_number)))
            if max_valid_number is None or number > max_valid_number:
                max_valid_number = number
                print(f"{number} is the new max")


def create_dataset(n: int = int(1e3)):
    X = gen_fourteen_digit_number(n)
    y = np.zeros((n))
    for i, fourteen_digit_number in enumerate(iter(X)):
        if i % 1000 == 0:
            print(i)
        alu = Alu(commands=commands, inputs=list(fourteen_digit_number))
        alu.execute_commands()
        y[i] = alu.z
    return X, y


def part1_via_prio_queue():
    # We know that each input can only be in range(1, 10)
    # use each one as input and see how values for each of x, y, z, w change. possible maybe are the same for each input
    pq = PriorityQueue()
    alu = Alu(commands, inputs=list())
    pq.put((0, alu))
    digits = list(range(9, 0, -1))
    n_checked = 0
    while pq:
        _, alu = pq.get()

        # add another digit to the object with the best priority
        for digit in digits:
            new_object = deepcopy(alu)
            new_object.inputs.append(digit)
            runs_correct = new_object.execute_commands()

            if n_checked % 10000 == 0:
                print(n_checked)
                print(new_object.inputs)
            n_checked += 1

            if runs_correct:
                prio = -1 * int(''.join(map(str, new_object.inputs)))
                pq.put((prio, new_object))


def part1_via_string_alu():
    alu = StringAlu(commands=commands)
    alu.execute_commands()
    print(alu.z)
    print(len(alu.z))


if __name__ == '__main__':
#     # Sample data
#     SAMPLES = ("""inp x
# mul x -1""",
#                """inp z
# inp x
# mul z 3
# eql z x""",
#                """inp w
# add z w
# mod z 2
# div w 2
# add y w
# mod y 2
# div w 2
# add x w
# mod x 2
# div w 2
# mod w 2""")
#     for sample in SAMPLES:
#         commands = parse_data(sample)
#         alu = Alu(commands, inputs=[3, 3])
#         alu.execute_commands()
#         print(alu.z)
#
#     n = 13579246899999
#     inputs = map(int, str(n))
#     result = is_valid(inputs)
#     print(f'{n} is valid??', result)

    # Actual data
    RAW = load_data('input.txt')
    commands = parse_data(RAW)

    # Part 1
    # X, y = create_dataset()
    # plt.plot(y)
    # fig, ax = plt.subplots(1, 1)
    # plt.semilogy(y, ax=ax)
    # plt.savefig('test.png')
    # print(pd.Series(y).describe())

    # part1_via_prio_queue()

    part1_via_string_alu()
