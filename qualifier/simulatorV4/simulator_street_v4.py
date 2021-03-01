from collections import deque


class SimulatorStreetV4:
    def __init__(self, length: int, passing_times: deque):
        self.length = length
        self.passing_times = passing_times  # green light times
