from typing import Tuple

from qualifier.schedule import Schedule


class OutputData:
    def __init__(self, schedules: Tuple[Schedule]):
        """ raw_data can be left empty, if it is easier to construct it during solving... """
        if not isinstance(schedules, tuple):
            raise ValueError(f'Should be an immutable tuple for Schedule but was {type(schedules)}')

        self.schedules = schedules

    def save(self, filename: str):
        final_schedules = [schedule for schedule in self.schedules if len(schedule.street_duration_tuples) > 0]

        text = f'{len(final_schedules)}\n'
        for schedule in final_schedules:
            text += str(schedule)

        with open(filename, 'w') as file:
            file.write(text)
