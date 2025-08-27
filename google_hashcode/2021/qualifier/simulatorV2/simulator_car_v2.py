from typing import List



class SimulatorCarV2:
    def __init__(self, path: List[str]):
        self.path = path.copy()
        self.name = f'{path[0]} to {path[-1]}'

    def __str__(self):
        return self.name
