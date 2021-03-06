from collections import deque

from qualifier.simulatorV5.traffic_light import TrafficLight, green_light_times


class SimulatorStreetV5:
    def __init__(self, length: int):
        self.length = length
        self.passing_times = green_light_times(0, 0, 0, -1)  # green light times
        self.n_unused_passing_times = 0
        self.sum_waiting_time = 0

    def clear(self):
        self.passing_times = green_light_times(0, 0, 0, -1)
        self.n_unused_passing_times = 0
        self.sum_waiting_time = 0
