from typing import List, Tuple
from itertools import product


def load_data(filename: str) -> str:
    with open(filename, 'r') as f:
        return f.read()


def parse_data(raw_data: str):
    commands = []
    for line in raw_data.splitlines():
        commands.append(line.split())
    return commands


class Alu:
    def __init__(self, commands: List[List[str]], inputs: List[int]):
        self.x = 0
        self.y = 0
        self.z = 0
        self.w = 0
        self.commands = commands
        self.inputs = inputs

    def __repr__(self):
        return f"{self.x}, {self.y}, {self.z}, {self.w}"

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
        return a // b

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
        for cmd in self.commands:
            instruction = cmd[0]
            var = cmd[1]
            if instruction == 'inp':
                value = self.inputs.pop(0)
                assert 1 <= value <= 9, f"{value} is not in range"
                setattr(self, var, value)
            elif instruction in ['add', 'mul', 'mod', 'div', 'eql']:
                func = getattr(self, instruction)
                try:
                    value = int(cmd[2])
                except ValueError:
                    value = getattr(self, cmd[2])
                setattr(self, var, func(getattr(self, var), value))
            else:
                raise ValueError(f"Unknown instruction {instruction}.")


def part1():
    commands = parse_data(RAW)
    max_number = None
    for i, fourteen_digit_number in enumerate(product(range(1, 10), repeat=14)):
        if i < 1514000:
            continue
        if i % 1000 == 0:
            print(i)
        alu = Alu(commands, inputs=list(fourteen_digit_number))
        alu.execute_commands()
        print('z', alu.z)
        if alu.z == 0:
            # Valid fourteen digit number
            number = int(''.join(map(str, fourteen_digit_number)))
            if max_number is None or number > max_number:
                max_number = number
                print(f"{number} is the new max")


if __name__ == '__main__':
    # Sample data
    SAMPLES = ("""inp x
mul x -1""",
               """inp z
inp x
mul z 3
eql z x""",
               """inp w
add z w
mod z 2
div w 2
add y w
mod y 2
div w 2
add x w
mod x 2
div w 2
mod w 2""")
    for sample in SAMPLES:
        commands = parse_data(sample)
        alu = Alu(commands, inputs=[3, 3])
        alu.execute_commands()

    # Actual data
    RAW = load_data('input.txt')
    data = parse_data(RAW)
    part1()

    # Part 1

    # Part 2
