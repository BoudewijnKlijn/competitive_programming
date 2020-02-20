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


def strategy_0(problem):
    """
    dumbest strategy
    start with first library, import books in default order. no smart stuff
    """
    output = list()
    for library_i, library in enumerate(problem.libraries):
        output.append((library_i, []))
        for book_i, book in enumerate(library.books):
            output[library_i][1].append(book.id)
    return output


def strategy_1(problem):
    """
    just start with the first library.
    sort books on value
    """
    output = list()
    for library_i, library in enumerate(problem.libraries):
        output.append((library_i, []))
        for book_i, book in enumerate(sorted(library.books, key=lambda x: x.score, reverse=True)):
            output[library_i][1].append(book.id)
    return output


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


def create_submission_file(output, filename_out='out.txt'):
    with open(filename_out, 'w') as f:
        f.write(f'{len(output)}\n')
        for i, (library_id, books) in enumerate(output):
            f.write(f'{library_id} {len(books)}\n')
            f.write(' '.join([str(book_id) for book_id in books]))

            if i != len(output) - 1:
                f.write('\n')


def main():
    files = ['a_example.txt', 'b_read_on.txt', 'c_incunabula.txt', 'd_tough_choices.txt', 'e_so_many_books.txt',
             'f_libraries_of_the_world.txt']

    for file in files:
        # file = 'a_example.txt'
        file_out = 'out_' + file

        loaded = load_file(file)
        # print(loaded)
        # print(loaded.books)
        # print(loaded.libraries)

        # output = strategy_0(loaded)  # 10495004
        output = strategy_1(loaded)  # 10750360

        create_submission_file(output, file_out)


def calc_total_score_per_library(settings, libraries, books):
    """
    D = number of days
    D - signup_time
    """



if __name__ == '__main__':
    main()
