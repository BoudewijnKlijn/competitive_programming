from valcon import OutputData


class CarSchedule:
    nr_of_rides: int
    rides: [int]


class CarSchedules(OutputData):
    def __init__(self, car_schedules: [CarSchedule]):
        self.car_schedules = car_schedules
        
    def save(self, filename: str):
        pass
