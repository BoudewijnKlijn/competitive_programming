import timeit

from copy import deepcopy

from collections import deque


n_street_duration_tuples = 50  # todo: should be average streets per intersection
street_duration_tuples = tuple((str(i), i) for i in range(1, n_street_duration_tuples))


def sum1():
    return sum([d for _, d in street_duration_tuples])


def sum2():
    return sum(list(zip(*street_duration_tuples))[1])


# number = 100000
# print(timeit.timeit('sum1()',  number=number, globals=globals()))
# print(timeit.timeit('sum2()', number=number, globals=globals()))


DURATION = 10000


def green_light_times1():
    sum_other_streets_before = 0
    length_schedule = sum([d for _, d in street_duration_tuples])
    results = list()
    for street_name, duration in street_duration_tuples:
        result = deque([time for time in [
            sum_other_streets_before +
            seconds_this_street_before +
            length_schedule * multiplier
            for multiplier in range(2 + DURATION // length_schedule)
            for seconds_this_street_before in range(duration)
        ] if time < DURATION])
        sum_other_streets_before += duration
        results.append(result)
    return results


def green_light_times2():
    sum_other_streets_before = 0
    length_schedule = sum([d for _, d in street_duration_tuples])
    results = list()
    for street_name, duration in street_duration_tuples:
        times = list()
        for seconds_this_street_before in range(duration):
            times += range(sum_other_streets_before + seconds_this_street_before,
                           DURATION,
                           length_schedule)
        sum_other_streets_before += duration
        results.append(deque(sorted(times)))
    return results


from itertools import chain


def green_light_times21():
    sum_other_streets_before = 0
    length_schedule = sum([d for _, d in street_duration_tuples])
    results = list()
    for street_name, duration in street_duration_tuples:
        ranges = (range(sum_other_streets_before + seconds_this_street_before,
                           DURATION,
                           length_schedule) for seconds_this_street_before in range(duration))
        sum_other_streets_before += duration
        results.append(deque(sorted(chain(*ranges))))
    return results


import numpy as np


def green_light_times22():
    sum_other_streets_before = 0
    length_schedule = sum([d for _, d in street_duration_tuples])
    results = list()
    for street_name, duration in street_duration_tuples:
        times = np.sort(
            np.concatenate(
                [np.arange(sum_other_streets_before + seconds_this_street_before,
                           DURATION,
                           length_schedule
                           ) for seconds_this_street_before in range(duration)
                 ]
            ), kind='stable'
        )
        # list()
        # for seconds_this_street_before in range(duration):
        #     times += range(sum_other_streets_before + seconds_this_street_before,
        #                    DURATION,
        #                    length_schedule)
        sum_other_streets_before += duration
        results.append(deque(times))
    return results


def green_light_times3():
    sum_other_streets_before = 0
    length_schedule = sum([d for _, d in street_duration_tuples])
    results = list()
    for street_name, duration in street_duration_tuples:
        times = list()
        for seconds_this_street_before in range(duration):
            times.append(range(sum_other_streets_before + seconds_this_street_before,
                           DURATION,
                           length_schedule).__iter__())

        sum_other_streets_before += duration

        sorted_times = list()
        while times:
            try:
                for iterrange in times:
                    sorted_times.append(next(iterrange))
            except StopIteration:
                break
        results.append(deque(sorted_times))
    return results


assert green_light_times1() == green_light_times2()
# assert green_light_times2() == green_light_times21()
assert green_light_times1() == green_light_times3()


number = 1000
print(timeit.timeit('green_light_times1()',  number=number, globals=globals()))
print(timeit.timeit('green_light_times2()',  number=number, globals=globals()))
print(timeit.timeit('green_light_times3()',  number=number, globals=globals()))
print(timeit.timeit('green_light_times21()',  number=number, globals=globals()))
print(timeit.timeit('green_light_times22()',  number=number, globals=globals()))


size = 1000000
L = list(range(size))
Q = deque(deepcopy(L))
L_reversed = deepcopy(L)[::-1]
L_iter = deepcopy(L).__iter__()


def loop1():
    for x in L:
        # print(x)
        x * 2  # some operation


def loop2():
    while True:
        try:
            x = Q.popleft()
        except IndexError:
            break
        # print(x)
        x * 2  # some operation


def loop3():
    while True:
        try:
            x = L_reversed.pop()
        except IndexError:
            break
        # print(x)
        x * 2  # some operation


def loop4():
    while True:
        try:
            x = next(L_iter)
        except StopIteration:
            break
        # print(x)
        x * 2  # some operation


# number = 1
# print(timeit.timeit('loop1()',  number=number, globals=globals()))
# print(timeit.timeit('loop2()',  number=number, globals=globals()))
# print(timeit.timeit('loop3()',  number=number, globals=globals()))
# print(timeit.timeit('loop4()',  number=number, globals=globals()))


# inner_list_size = 100
# n_lists = 10000
# L = list([list(range(inner_list_size)) for _ in range(n_lists)])
# Q = list([deque(range(inner_list_size)) for _ in range(n_lists)])
# L_iter = list([iter(range(inner_list_size)) for _ in range(n_lists)])


def loop21():
    for inner in L:
        for x in inner:
            # print(x)
            x * 2  # some operation


def loop22():
    for inner in Q:
        while True:
            try:
                x = inner.popleft()
            except IndexError:
                break
            # print(x)
            x * 2  # some operation


def loop24():
    for inner in L_iter:
        while True:
            try:
                x = next(inner)
            except StopIteration:
                break
            # print(x)
            x * 2  # some operation


# number = 1
# print(timeit.timeit('loop21()',  number=number, globals=globals()))
# print(timeit.timeit('loop22()',  number=number, globals=globals()))
# print(timeit.timeit('loop24()',  number=number, globals=globals()))