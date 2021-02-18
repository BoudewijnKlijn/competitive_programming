class InputData:

    def __init__(self, filename: str):
        with open(filename) as file:
            lines = file.readlines()

        self.data = lines

    def get_data(self):
        return self.data
