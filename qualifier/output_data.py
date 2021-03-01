from typing import Tuple

from qualifier.schedule import Schedule


class OutputData:
    def __init__(self, schedules: Tuple[Schedule]):
        """ raw_data can be left empty, if it is easier to construct it during solving... """
        if not isinstance(schedules, tuple):
            raise ValueError(f'Should be an immutable tuple for Schedule but was {type(schedules)}')

        self.schedules = schedules

    def save(self, filename: str):
        final_schedules = [str(schedule) for schedule in self.schedules if len(schedule.street_duration_tuples) > 0]
        final_schedules = [schedule for schedule in final_schedules if schedule != '']

        text = f'{len(final_schedules)}\n'
        for schedule in final_schedules:
            text += str(schedule)

        with open(filename, 'w') as file:
            file.write(text)

    @classmethod
    def read(cls, filename: str):
        print(f'Warning this will not yet fill in duration 0 / missing street lights that were permanent red')
        print(f'Will also not add missing intersections')
        with open(filename, 'r') as file:
            lines = file.readlines()

        schedules = []

        intersections = int(lines.pop(0))
        while (lines):
            intersection = int(lines.pop(0).strip())
            schedule_count = int(lines.pop(0).strip())
            street_durations = []
            for _ in range(schedule_count):
                street, duration = lines.pop(0).split(' ')
                street_durations.append((street, int(duration.strip())))

            schedules.append(Schedule(intersection, tuple(street_durations)))
        return OutputData(tuple(schedules))
