from collections import deque


class SimulatorCarV4:
    def __init__(self, path):
        self.path = deque([street.name for street in path])
        self.time_passed = 0

    def __repr__(self):
        return f'{self.time_passed=}, {self.path=}'
