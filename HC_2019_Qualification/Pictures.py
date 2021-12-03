from HC_2019_Qualification.picture import Picture
from valcon import InputData


class Pictures(InputData):

    def __init__(self, file_name: str):
        with open(file_name, 'r') as file:
            number, *lines = file.readlines()

        self.n_pictures = int(number)
        self.pictures = [Picture(index, line) for index, line in enumerate(lines)]
