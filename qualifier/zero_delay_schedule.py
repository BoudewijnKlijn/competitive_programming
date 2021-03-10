"""Helper to verify if it possible to create a schedule with no delays for lists of arrival times at incoming
streets. If it is possible, such a schedule is returned."""


from typing import List, Tuple
from itertools import chain
from collections import defaultdict


D = 8071  # duration of D


def get_zero_delay_schedule(arrivals: List[List[int]]):
    """Verify if it is possible to create a schedule to delays none of the incoming cars.
     Return None if impossible."""

    # if arrivals contains duplicates, then its impossible create a zero delay schedule
    if len(set(chained := list(chain.from_iterable(arrivals)))) != len(chained):
        return None

    minimum_cycle_length = len(arrivals)  # when all lights are green for one second
    maximum_cycle_length = D  # todo: decrease upper bound

    def has_uninterrupted_periods(min_max_per_street):
        """Green light of one street must not be interrupted by green light of another street within schedule.
        # We rely on min_max_per_street being created with values being sorted."""
        min_maxes = list(min_max_per_street.values())
        for (min_street1, max_street1), (min_street2, max_street2) in zip(min_maxes[:-1], min_maxes[1:]):
            if max(min_street1, min_street2) <= min(max_street1, max_street2):
                return False
        return True

    def create_schedule(min_max: dict, schedule_length: int) -> List[Tuple[str, int]]:
        """Create schedule. Start from 0 with green until the max of first. Then green until max of second. Etc.
        Last duration is corrected to make sure the sum of all duration == schedule_length."""
        created_schedule = list()
        prev_max = -1
        for street_name, (min_, max_) in min_max.items():
            duration_on = max_ - prev_max
            created_schedule.append((street_name, duration_on))
            prev_max = max_

        # Adjust last street. The total schedule needs to have the predetermined schedule length
        duration_correction = schedule_length - (prev_max + 1)
        last_street = created_schedule.pop()
        last_street = (last_street[0], last_street[1] + duration_correction)
        created_schedule.append(last_street)
        return created_schedule

    for try_cycle_length in range(minimum_cycle_length, maximum_cycle_length):
        remainders = [[arrival % try_cycle_length for arrival in street] for street in arrivals]
        min_max_remainder_per_street = [
            (min(arrival_remainders_one_street), max(arrival_remainders_one_street), str(street_name))
            for street_name, arrival_remainders_one_street in enumerate(remainders)
        ]
        # It's important to sort here for some efficiency gains!
        min_max_dict = {street_name: (min_, max_) for min_, max_, street_name in sorted(min_max_remainder_per_street)}
        if has_uninterrupted_periods(min_max_dict):
            return create_schedule(min_max_dict, try_cycle_length)
    return None


def visualize_schedule(street_duration_tuples, arrivals):
    if schedule is None:
        return

    chained = list(chain.from_iterable(arrivals))
    DURATION = max(chained) + 1
    result = defaultdict(list)
    all_times = list(range(DURATION))
    time = 0
    while time < DURATION:
        for street_name, duration, in street_duration_tuples:
            result[street_name] += all_times[time: (time := time + duration)]
    print(f'{result=}')


if __name__ == '__main__':
    test_cases = list()
    test_cases.append([[0]])
    test_cases.append([[0], [1]])
    test_cases.append([[0, 1, 2], [1]])
    test_cases.append([[0, 1, 2], [3]])
    test_cases.append([[1, 2, 3], [0]])
    test_cases.append([[1, 2, 3], [0], [18]])
    test_cases.append([[1, 2, 3], [0], [17]])
    test_cases.append([[1, 2, 3], [0], [16]])
    test_cases.append([[1, 2, 3], [0], [15]])

    for test_case in test_cases:
        schedule = get_zero_delay_schedule(test_case)
        print(f'\n{test_case=}, {schedule=}')
        visualize_schedule(street_duration_tuples=schedule, arrivals=test_case)
