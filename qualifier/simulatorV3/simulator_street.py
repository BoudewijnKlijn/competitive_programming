from collections import deque


class SimulatorStreetV3:
    def __init__(self, exit_intersection: int, length: int, name: str):
        self.length = length
        self.exit_intersection = exit_intersection
        self.has_green = False
        self.cars = deque()
        self.name = name

    def add_car(self, car, at_traffic_light=False):
        car.path = car.path[1:]  # remove current street

        if at_traffic_light:
            self.cars.append((car, 0))
        else:
            self.cars.append((car, self.length))  # car's can move 1 step when they move on to it.

    def set_green_light(self, green: bool):
        self.has_green = green

    def execute_timestep(self):
        # move all cars 1 step closer to the traffic light
        for i, car in enumerate(self.cars):
            self.cars[i] = (car[0], max(0, car[1] - 1))

        destination_reached = []
        for car in self.cars:
            if car[1] == 0 and len(car[0].path) == 0:
                destination_reached.append(car)
        for car in destination_reached:
            self.cars.remove(car)

        if self.has_green:
            if self.cars and self.cars[0][1] == 0:
                leaving_car = self.cars.popleft()[0]
            else:
                leaving_car = None
            return destination_reached, leaving_car
        else:
            return destination_reached, None

    def __str__(self):
        return self.name
