from dataclasses import dataclass

from valcon import OutputData


@dataclass
class CarSchedule:
    nr_of_rides: int
    rides: [int]

    def __repr__(self):
        return str(self.rides)


class CarSchedules(OutputData):
    def __init__(self, car_schedules: [CarSchedule]):
        self.car_schedules = car_schedules

    def save(self, filename: str):
        with open(filename, 'w') as file:
            for schedule in self.car_schedules:
                file.write(f"{schedule.nr_of_rides} {' '.join(schedule.rides)}\n")

    def __repr__(self):
        return f"CarSchedules {self.car_schedules}"
