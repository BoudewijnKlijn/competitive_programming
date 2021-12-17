import re
from collections import defaultdict
from itertools import product
from typing import Tuple


def load_data(filename: str) -> str:
    with open(filename, 'r') as f:
        return f.read()


def parse_data(raw_data: str) -> Tuple[int, int, int, int]:
    pattern = r'[-\d]+'
    x_min, x_max, y_min, y_max = map(int, re.findall(pattern, raw_data.strip()))
    return x_min, x_max, y_min, y_max


def determine_valid_starting_velocities(minimum: int, maximum: int, is_x: bool):
    """X velocity decreases or increases with 1 per step towards 0.
    Y velocity always decreases with 1 per step.
    We can determine all x starting velocities that:
    - stay on an x goal coordinate forever
    - are on an x goal coordinate for a single step
    Both are fine:
    - if forever, it can accommodate many y starting velocities
    - if one step, then the number of steps must match a specific y starting velocity that is in the grid after the same
    number of steps."""
    valid_starting_velocities_for_n_steps = defaultdict(set)
    for goal in range(minimum, maximum + 1):
        if is_x:
            starting_velocity_step = -1 if goal > 0 else 1
            starting_velocity_start = goal
            starting_velocity_stop = 0
        else:
            starting_velocity_step = -1
            starting_velocity_start = max(abs(minimum) + 1, abs(minimum) + 1)  # todo: this may not be correct. can increase this a lot and it still runs fast
            starting_velocity_stop = min(0, goal-1)
        for starting_velocity in range(starting_velocity_start, starting_velocity_stop, starting_velocity_step):
            # how many steps do we need to get to the goal?
            n_steps = 0
            position = 0
            velocity = starting_velocity
            while (is_x and abs(position) <= abs(goal)) or (not is_x and position >= goal):
                # keep iterating:
                # for x as long as position is between start and goal
                # for y as long as y is larger than goal
                n_steps += 1
                position += velocity
                if is_x:
                    velocity = velocity - 1 if velocity > 0 else velocity + 1
                else:
                    velocity -= 1
                if position == goal:
                    # we found a valid starting velocity
                    valid_starting_velocities_for_n_steps[n_steps].add(starting_velocity)
                    break
                if is_x and velocity == 0:
                    # if we are not yet at the goal, but have reached x velocity of zero, we can't get there
                    break
    return valid_starting_velocities_for_n_steps


def get_valid_starting_velocities():
    valid_starting_velocities = set()

    # Find x velocities that can get us to the target area (only need to consider the x range)
    x_valid_starting_velocities_for_n_steps = determine_valid_starting_velocities(x_min, x_max, is_x=True)

    y_valid_starting_velocities_for_n_steps = determine_valid_starting_velocities(y_min, y_max, is_x=False)

    # match x and y velocities that have the same number of steps
    common_steps = set(x_valid_starting_velocities_for_n_steps.keys()).intersection(
        set(y_valid_starting_velocities_for_n_steps.keys()))
    for n_steps in common_steps:
        for vx, vy in product(x_valid_starting_velocities_for_n_steps[n_steps],
                              y_valid_starting_velocities_for_n_steps[n_steps]):
            valid_starting_velocities.add((vx, vy))

    # use the valid x starting velocities that end with zero speed, those can be used with any y starting velocity that
    # has more steps than the x starting velocity
    for x_n_steps, x_starting_velocities in x_valid_starting_velocities_for_n_steps.items():
        for x_starting_velocity in x_starting_velocities:
            if x_n_steps == x_starting_velocity:
                # we found an x starting velocity that ends with zero speed
                for y_n_steps, y_starting_velocities in y_valid_starting_velocities_for_n_steps.items():
                    if y_n_steps >= x_n_steps:
                        for y_starting_velocity in y_starting_velocities:
                            valid_starting_velocities.add((x_starting_velocity, y_starting_velocity))
    return valid_starting_velocities


def part1():
    max_altitude = 0
    for _, vy in valid_starting_velocities:
        altitude = 0
        while vy > 0:
            altitude += vy
            vy -= 1
            if altitude > max_altitude:
                max_altitude = altitude
    return max_altitude


def part2():
    return len(valid_starting_velocities)


if __name__ == '__main__':
    # Sample data
    RAW = """target area: x=20..30, y=-10..-5"""
    x_min, x_max, y_min, y_max = parse_data(RAW)
    valid_starting_velocities = get_valid_starting_velocities()

    # Assert solution is correct
    assert part1() == 45
    assert part2() == 112

    # Actual data
    RAW = load_data('day17.txt')
    x_min, x_max, y_min, y_max = parse_data(RAW)
    valid_starting_velocities = get_valid_starting_velocities()

    # Part 1
    print(f'Part 1: {part1()}')

    # Part 2
    print(f'Part 2: {part2()}')
