import numpy as np
from collections import namedtuple
import matplotlib.pyplot as plt
from time import time


class Problem:
    def __init__(self, books=None, libraries=None, scanning_days=None):
        self.books = books
        self.libraries = libraries
        self.scanning_days = scanning_days

    def __repr__(self):
        return '< Problem \n\tBooks:{} \n\tLibraries:{} \n\tScanning days:{}'.format(self.books, self.libraries, self.scanning_days)

class Book:
    def __init__(self, id, score):
        self.id = id
        self.score = score

    def __repr__(self):
        return '<Book id:{} score:{}'.format(self.id, self.score)


class Library:
    def __init__(self, id=None, nr_books=None, books=None, signup_time=None, scanned_daily=None):
        self.id = id
        self.nr_books = nr_books
        self.books = books
        self.signup_time = signup_time
        self.scanned_daily = scanned_daily

    def __repr__(self):
        return '\n\t<Library \n\t\tid:{} \n\t\tnr_books:{} \n\t\tbooks:{} \n\t\tsignup_time:{} \n\t\tscanned_daily:{}'.format(self.id, self.nr_books, self.books, self.signup_time, self.scanned_daily)


def load_file(filename):
    library_id = 0

    with open(filename, 'r') as f:
        #file_read = f.read().strip()
        for idx, line in enumerate(f.readlines()):
            values = line.split()
            if idx == 0:
                [nr_books, nr_libraries, nr_days] = values
            elif idx == 1:
                books = {int(index): Book(id = int(index), score = int(index_score)) for index, index_score in enumerate(values)}
                problem = Problem(books=books, scanning_days=nr_days)
                problem.libraries = []
            else:
                if idx % 2 == 0:
                    # Even line numbers => first line of L sections
                    nr_books_in_library, signup_time_library, shipped_per_day_library = values
                    library = Library(id=library_id, nr_books=nr_books_in_library, signup_time=signup_time_library, scanned_daily=shipped_per_day_library)
                    library_id += 1
                else:
                    library.books = [problem.books[int(book_id)] for book_id in values]
                    problem.libraries.append(library)

    return problem


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
    file = 'data/a_example.txt'
    loaded = load_file(file)
    print(loaded)

if __name__ == '__main__':
    main()
