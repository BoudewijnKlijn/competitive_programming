import random


class Input:
    def __init__(self, n_min_max, val_min_max):
        self.n_min_max = n_min_max
        self.val_min_max = val_min_max


class InputList(Input):
    def __init__(self, n_min_max, val_min_max):
        super().__init__(n_min_max, val_min_max)


class InputInteger(Input):
    def __init__(self, val_min_max):
        super().__init__((1, 1), val_min_max)


def generate_testcases(structure, n=1, data_file=None, solver=None):
    for _ in range(n):
        # generate input data
        input_variables = list()
        for input_ in structure:
            if isinstance(input_, InputList):
                size = random.randint(*input_.n_min_max)
                input_variables.append(
                    [random.randint(*input_.val_min_max) for _ in range(size)]
                )
            elif isinstance(input_, InputInteger):
                input_variables.append(random.randint(*input_.val_min_max))

        # generate result
        result = -1
        if solver:
            result = solver(*input_variables)

        # write to file
        if data_file:
            with open(data_file, "a") as fp:
                output = (
                    f"{",".join(map(str,input_variables)).replace(" ","")}->{result}\n"
                )
                fp.write(output)

    return input_variables, result
