from valcon import OutputData


class Solution(OutputData):
    def __init__(self, data: dict):
        pass

    def save(self, filename: str):
        with open(filename, 'w') as file:
            pass
