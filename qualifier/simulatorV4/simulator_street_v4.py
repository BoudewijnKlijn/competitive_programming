from collections import deque


class SimulatorStreetV4:
    def __init__(self, length: int, passing_times: deque):
        self.length = length
        self.passing_times = passing_times  # green light times
        self.n_unused_passing_times = 0
        self.sum_waiting_time = 0
        self.arrival_times_car_at_light = list()
