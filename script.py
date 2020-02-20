import numpy as np
from collections import namedtuple
import matplotlib.pyplot as plt
from time import time


def load_file(filename):
    with open(filename, 'r') as f:
        return f.read().strip()


def create_submission_file(rides_all_cars, filename_out='out.txt'):
    with open(filename_out, 'w') as f:
        for i, rides_one_car in enumerate(rides_all_cars):
            if rides_one_car:
                f.write(f'{str(len(rides_one_car))} {" ".join([str(r) for r in rides_one_car])}')
            else:
                f.write('0')

            if i != len(rides_all_cars) - 1:
                f.write('\n')


def strategy_0():
    """
    dumbest strategy
    start with first library, import books in default order. no smart stuff
    """


def strategy_1():
    """
    just start with the first library.
    sort books on value
    """


def strategy_2():
    """
    sort libraries on total value that can be achieved within simulation time
    sort books on value
    """


def strategy_3():
    """
    sort libraries on total value that can be achieved within simulation time
    sort books on value
    start with a libraries that have short signup, and slow shipping time
    """


def strategy_4():
    """
    sort libraries on total value that can be achieved within simulation time
    sort books on value
    start with a libraries that have short signup, and slow shipping time

    """

# TODO / thoughts
# how to deal with uniqueness of books?
# calculate how many days you need to achieve 80%/90% of library value


def main():
    pass


def calc_total_score_per_library(settings, libraries, books):
    """
    D = number of days
    D - signup_time
    """



if __name__ == '__main__':
    main()
