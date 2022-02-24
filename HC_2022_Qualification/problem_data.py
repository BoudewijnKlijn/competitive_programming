from valcon import InputData


class ProblemData(InputData):
    def __init__(self, file_name: str):
        with open(file_name, 'r') as file:
            meta_data, *raw_data = file.readlines()

        self.
