from dataclasses import dataclass

from valcon import OutputData


@dataclass
class CarSchedule:
    nr_of_rides: int
    rides: [int]


class CarSchedules(OutputData):
    def __init__(self, car_schedules: [CarSchedule]):
        self.car_schedules = car_schedules

    def save(self, filename: str):
        with open(filename, 'w') as file:
            for schedule in self.car_schedules:
                file.write(f"{schedule.nr_of_rides} {' '.join(schedule.rides)}\n")
