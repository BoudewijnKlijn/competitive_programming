class OutputData:
    def __init__(self, raw_data=None):
        """ raw_data can be left empty, if it is easier to construct it during solving... """
        self.data = raw_data

    def save(self, filename: str):
        with open(filename, 'w') as file:
            file.writelines(self.data)
