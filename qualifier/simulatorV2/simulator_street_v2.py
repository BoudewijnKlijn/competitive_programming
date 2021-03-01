from collections import deque


class SimulatorStreetV2:
    def __init__(self, exit_intersection: int, length: int, name: str):
        self.length = length
        self.exit_intersection = exit_intersection
        self.cars = deque()
        self.name = name
        self.schedule_duration = 0  # 0 to skip if this street had no schedule...
        self.green_start = None
        self.green_end = None

    def add_car(self, car, at_traffic_light=False):
        car.path = car.path[1:]  # remove current street

        if at_traffic_light:
            self.cars.append((car, 0))
        else:
            self.cars.append((car, self.length))  # car's can move 1 step when they move on to it.

    def set_schedule(self, schedule_duration: int, start: int, end: int):
        self.schedule_duration = schedule_duration
        self.green_start = start
        self.green_end = end

    def execute_timestep(self, time):
        # move all cars 1 step closer to the traffic light
        for i, car in enumerate(self.cars):
            self.cars[i] = (car[0], max(0, car[1] - 1))

        destination_reached = []
        for car in self.cars:
            if car[1] == 0 and len(car[0].path) == 0:
                destination_reached.append(car)
        for car in destination_reached:
            self.cars.remove(car)

        if self.schedule_duration == 0:
            return destination_reached, None

        has_green = self.green_start <= time % self.schedule_duration < self.green_end
        if has_green:
            if self.cars and self.cars[0][1] == 0:
                leaving_car = self.cars.popleft()[0]
            else:
                leaving_car = None
            return destination_reached, leaving_car
        else:
            return destination_reached, None

    def __str__(self):
        return self.name
