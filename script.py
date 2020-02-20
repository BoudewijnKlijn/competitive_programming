import numpy as np
from collections import namedtuple
import matplotlib.pyplot as plt
from time import time
from collections import Counter


class Problem:
    def __init__(self, books=None, libraries=None, scanning_days=None):
        self.books = books
        self.libraries = libraries
        self.scanning_days = int(scanning_days)

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
        self.id = int(id)
        self.nr_books = int(nr_books)
        self.books = books
        self.signup_time = int(signup_time)
        self.scanned_daily = int(scanned_daily)

    def __repr__(self):
        return '\n\t<Library \n\t\tid:{} \n\t\tnr_books:{} \n\t\tbooks:{} \n\t\tsignup_time:{} \n\t\tscanned_daily:{}'.format(self.id, self.nr_books, self.books, self.signup_time, self.scanned_daily)


def load_input_file(filename):
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
        output.append((library.id, []))
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
        output.append((library.id, []))
        for book_i, book in enumerate(sorted(library.books, key=lambda x: x.score, reverse=True)):
            output[library_i][1].append(book.id)
    return output


def strategy_2(problem):
    """
    sort libraries on total value that can be achieved within simulation time
    sort books on value
    """
    output = list()
    max_score_library = calc_total_score_per_library(problem)

    sorted_libraries = [library for _, (_, library) in sorted(zip(max_score_library, enumerate(problem.libraries)), reverse=True)]

    for library_i, library in enumerate(sorted_libraries):
        output.append((library.id, []))
        for book_i, book in enumerate(sorted(library.books, key=lambda x: x.score, reverse=True)):
            output[library_i][1].append(book.id)
    return output


def strategy_3(problem):
    """
    sort books on value
    sort libraries on ascending ratio signup time / total shipping time
    """
    output = list()
    time_ratios_library = calc_ratio_signup_shipping_per_library(problem)

    sorted_libraries = [library for _, (_, library) in sorted(zip(time_ratios_library, enumerate(problem.libraries)))]

    for library_i, library in enumerate(sorted_libraries):
        output.append((library.id, []))
        for book_i, book in enumerate(sorted(library.books, key=lambda x: x.score, reverse=True)):
            output[library_i][1].append(book.id)
    return output


def strategy_4(problem):
    """
    sort libraries on ascending ratio signup time / total shipping time
    sort books on value
    put unique books first
    """

    # get all books
    all_books = []

    for library in problem.libraries:
        library_book_ids = [book.id for book in library.books]
        all_books.extend(library_book_ids)

    books_counter = Counter(all_books)

    output = list()
    time_ratios_library = calc_ratio_signup_shipping_per_library(problem)

    sorted_libraries = [library for _, (_, library) in sorted(zip(time_ratios_library, enumerate(problem.libraries)))]


    for library_i, library in enumerate(sorted_libraries):
        output.append((library.id, []))
        library_books = library.books

        library_unique_books = [book for book in library.books if books_counter[book.id] == 1]
        library_non_unique_books = [book for book in library_books if not book in library_unique_books]

        for book_i, book in enumerate(sorted(library_unique_books, key=lambda x: x.score, reverse=True)):
            output[library_i][1].append(book.id)

        for book_i, book in enumerate(sorted(library_non_unique_books, key=lambda x: x.score, reverse=True)):
            output[library_i][1].append(book.id)

    return output


def strategy_5():
    """
    sort libraries on total value that can be achieved within simulation time
    sort books on value
    start with a libraries that have short signup, and slow shipping time

    """

# check for double book ids!

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

    for idx, file in enumerate(files):

        file_out = 'out_' + file

        loaded = load_input_file(file)
        # print(loaded)
        # print(loaded.books)
        # print(loaded.libraries)

        # output = strategy_0(loaded)  # 10495004
        # output = strategy_1(loaded)  # 10750360
        output = strategy_4(loaded)  # xxx

        create_submission_file(output, file_out)

        # if idx == 0:
        #     break


def analyse():
    file = 'a_example.txt'
    # file = 'b_read_on.txt'
    loaded = load_input_file(file)
    max_score_library = calc_total_score_per_library(loaded)

    print([j for _, j in sorted(zip(max_score_library, loaded.libraries), reverse=True)])
    # print(max_score_library)


def calc_total_score_per_library(problem):
    """
    D = number of days
    D - signup_time
    """
    D = problem.scanning_days
    max_score_library = list()
    for library in problem.libraries:
        max_possible_scan_time = D - library.signup_time
        max_possible_books_to_scan = max_possible_scan_time * library.scanned_daily
        sorted_book_scores = sorted([book.score for book in library.books], reverse=True)
        max_score_library.append(sum(sorted_book_scores[:max_possible_books_to_scan]))

    return max_score_library

def calc_ratio_signup_shipping_per_library(problem):
    D = problem.scanning_days
    ratio_time_library = list()
    for library in problem.libraries:
        # max_possible_scan_time = D - library.signup_time
        # max_possible_books_to_scan = max_possible_scan_time * library.scanned_daily
        # sorted_book_scores = sorted([book.score for book in library.books], reverse=True)
        # max_score_library.append(sum(sorted_book_scores[:max_possible_books_to_scan]))
        total_shipping_time = library.nr_books / library.scanned_daily

        ratio_signup_shipping = library.signup_time / total_shipping_time

        ratio_time_library.append(ratio_signup_shipping)
    return ratio_time_library

if __name__ == '__main__':
    main()
    # analyse()
