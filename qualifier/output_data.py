from typing import List

from qualifier.schedule import Schedule


class OutputData:
    def __init__(self, schedules: List[Schedule]):
        """ raw_data can be left empty, if it is easier to construct it during solving... """
        self.schedules = schedules

    def save(self, filename: str):
        text = f'{len(self.schedules)}\n'
        for schedule in self.schedules:
            text += str(schedule)

        with open(filename, 'w') as file:
            file.write(text)
