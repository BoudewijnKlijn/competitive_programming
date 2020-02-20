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
                

def main():
    pass


if __name__ == '__main__':
    main()
