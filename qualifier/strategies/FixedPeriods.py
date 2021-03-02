from qualifier.output_data import OutputData
from qualifier.schedule import Schedule
from qualifier.strategy import Strategy


class FixedPeriods(Strategy):
    name = 'FixedPeriods'

    def __init__(self, period=1):
        super().__init__()
        self.period = period

    def solve(self, input_data):
        schedules = []
        for intersection in input_data.intersections:
            trafic_lights = []
            for street in intersection.incoming_streets:
                trafic_lights.append((street.name, self.period))
            schedule = Schedule(intersection.index, tuple(trafic_lights))
            schedules.append(schedule)

        return OutputData(tuple(schedules))
