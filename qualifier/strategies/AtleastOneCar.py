from qualifier.output_data import OutputData
from qualifier.schedule import Schedule
from qualifier.strategy import Strategy


class AtleastOneCar(Strategy):
    name = 'AtleastOneCar'

    def solve(self, input):

        all_streets = [car.path for car in input.cars]
        streets_with_cars = {item for sublist in all_streets for item in sublist}

        schedules = []
        for intersection in input.intersections:
            trafic_lights = []
            for street in intersection.incoming_streets:
                if street.name in streets_with_cars:
                    trafic_lights.append((street.name, 1))

            schedule = Schedule(intersection.index, trafic_lights)
            schedules.append(schedule)

        return OutputData(tuple(schedules))
