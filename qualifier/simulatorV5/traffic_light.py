def green_light_times(cycle_length, green_start, green_end, duration):
    time = green_start
    green_length = green_end - green_start
    red_length = cycle_length - green_length

    while time < duration:
        remainder = time % cycle_length

        if remainder == green_end or (remainder != green_start and remainder == 0):
            time += red_length
        elif green_start <= remainder:
            for _ in range(green_length):
                yield time
                time += 1
