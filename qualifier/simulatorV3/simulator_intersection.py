from typing import List

from qualifier.schedule import Schedule
from qualifier.simulatorV3.simulator_street import SimulatorStreetV3


class SimulatorIntersectionV3:
    def __init__(self, intersection: int, streets: List[SimulatorStreetV3]):
        self.intersection_number = intersection
        self.schedule = []
        self.streets = []
        self.schedule_duration = 0
        self.actual_streets = {street.name: street for street in streets}
        self.green = 0

    def add_schedule(self, schedule: Schedule):
        self.schedule = []  # clear old schedule
        self.streets = []  # clear old streets

        for index, (street, duration) in enumerate(schedule.street_duration_tuples):
            if duration == 0:
                continue

            self.schedule += [index] * duration
            self.streets.append(self.actual_streets[street])

        self.schedule_duration = len(self.schedule)

    def _get_green(self, time):
        return self.schedule[time % self.schedule_duration]

    def execute_timestep(self, time):
        green = self._get_green(time)

        self.streets[self.green].set_green_light(False)
        self.streets[green].set_green_light(True)
        self.green = green
