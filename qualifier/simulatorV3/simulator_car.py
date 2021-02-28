from typing import List


class SimulatorCarV3:
    def __init__(self, path: List[str]):
        self.path = path
        self.name = f'{path[0]} to {path[-1]}'

    def __str__(self):
        return self.name
