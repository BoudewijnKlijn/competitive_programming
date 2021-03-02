from qualifier.output_data import OutputData
from qualifier.schedule import Schedule
from qualifier.strategy import Strategy


class FixedPeriods(Strategy):
    name = 'FixedPeriods'

    def solve(self, input):
        schedules = []
        for intersection in input.intersections:
            trafic_lights = []
            for street in intersection.incoming_streets:
                trafic_lights.append((street.name, 1))
            schedule = Schedule(intersection.index, tuple(trafic_lights))
            schedules.append(schedule)

        return OutputData(tuple(schedules))