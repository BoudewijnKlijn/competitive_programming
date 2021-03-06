from collections import Generator


class TrafficLight(Generator):
    def __init__(self, cycle_length, green_start, green_end, duration):
        self.duration = duration
        self.green_end = green_end
        self.green_start = green_start
        self.cycle_length = cycle_length
        self.time = 0  # this will start the loop with 0

    def __iter__(self):
        return self

    def __next__(self):
        while self.time < self.duration:
            if self.green_start <= self.time % self.cycle_length < self.green_end:
                yield self.time
            self.time += 1

        raise StopIteration()


def green_light_times(cycle_length, green_start, green_end, duration):
    time = 0
    while time < duration:
        if green_start <= time % cycle_length < green_end:
            yield time
        time += 1
