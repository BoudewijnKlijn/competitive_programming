
from qualifier.simulatorV5.traffic_light import green_light_times


class SimulatorStreetV5:
    __slots__ = ['length', 'passing_times', 'n_unused_passing_times', 'sum_waiting_time']

    def __init__(self, length: int):
        self.length = length
        self.passing_times = green_light_times(0, 0, 0, -1)  # green light times
        self.n_unused_passing_times = 0
        self.sum_waiting_time = 0

    def clear(self):
        self.passing_times = green_light_times(0, 0, 0, -1)
        self.n_unused_passing_times = 0
        self.sum_waiting_time = 0
