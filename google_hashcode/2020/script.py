# # TODO / thoughts
# # how to deal with uniqueness of books?
# # calculate how many days you need to achieve 80%/90% of library value
# # check for double book ids!


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import itertools
from collections import Counter


import helper


def strategy_0(problem):
    """
    dumbest strategy
    start with first library, import books in default order. no smart stuff
    """
    output = list()
    for library in problem.libraries:
        books = [book.id for book in library.books]
        output.append((library.id, books))

    return output


def strategy_1(problem):
    """
    just start with the first library.
    sort books on value
    """
    output = list()
    for library in problem.libraries:
        books = [book.id for book in sorted(library.books, key=lambda x: x.score, reverse=True)]
        output.append((library.id, books))
    return output


def strategy_2(problem):
    """
    optimal for B (all same value, unique books)
    sort books on value
    sort libraries on signup time, ascending
    """
    output = list()
    for library in sorted(problem.libraries, key=lambda x: x.signup_time):
        books = [book.id for book in sorted(library.books, key=lambda x: x.score, reverse=True)]
        output.append((library.id, books))
    return output


def strategy_3(problem):
    """
    sort books on value
    sort libraries on signup time, ascending
    skip duplicate books
    """
    output = list()
    all_book_ids = set()

    for library in sorted(problem.libraries, key=lambda x: x.signup_time):
        book_ids = [book.id for book in sorted(library.books, key=lambda x: x.score, reverse=True)
                    if book.id not in all_book_ids]

        output.append((library.id, book_ids))
        all_book_ids.update(book_ids)

    return output


def strategy_4(problem):
    """
    sort books on value
    sort libraries on signup time, ascending
    skip duplicate books
    stop adding books when time is up (to prevent ruining the book_ids set)
    """
    output = list()
    all_book_ids = set()

    remaining_days = problem.n_days

    for library in sorted(problem.libraries, key=lambda x: x.signup_time):
        remaining_days = remaining_days - library.signup_time
        if remaining_days <= 0:
            break

        book_ids = [book.id for book in sorted(library.books, key=lambda x: x.score, reverse=True)
                    if book.id not in all_book_ids]

        max_possible_books_to_scan = remaining_days * library.scanned_daily
        book_ids = book_ids[:max_possible_books_to_scan]
        if len(book_ids) <= 0:
            continue

        output.append((library.id, book_ids))
        all_book_ids.update(book_ids)

    return output


def strategy_5(problem):
    """
    try optimal for C (max 20 books in library, and min 210 scanned daily. so every library completes scanning in 1 day)
    book scores differ from 1 to 600 (uniformly distributed)
    balance total score of library with signup time.
    150k books, 78k is unique. some libraries can maybe be skipped due to overlapping books
    """
    output = list()
    remaining_days = problem.n_days

    max_score_libraries = np.array(calc_max_score_library(problem.libraries))
    signup_time_libraries = np.array([library.signup_time for library in problem.libraries])
    for _, library in sorted(zip(max_score_libraries/signup_time_libraries, problem.libraries), reverse=True):
        remaining_days = remaining_days - library.signup_time
        if remaining_days <= 0:
            break

        book_ids = [book.id for book in library.books]
        output.append((library.id, book_ids))
    return output


def strategy_6(problem):
    """
    try optimal for C (max 20 books in library, and min 210 scanned daily. so every library completes scanning in 1 day)
    book scores differ from 1 to 600 (uniformly distributed)
    balance total score of library with signup time.
    150k books, 78k is unique. some libraries can maybe be skipped due to overlapping books
    same as strat 5 but update the library scores based on what is submitted already.
    """
    output = list()
    remaining_days = problem.n_days

    unused_libraries = problem.libraries.copy()
    used_libraries = list()
    scanned_books = set()

    while remaining_days > 0:

        print(len(scanned_books))

        max_score_libraries = np.array(calc_max_score_library(unused_libraries, scanned_books))
        signup_time_libraries = np.array([library.signup_time for library in unused_libraries])

        for _, library in sorted(zip(max_score_libraries / signup_time_libraries, unused_libraries), reverse=True):
            remaining_days = remaining_days - library.signup_time
            if remaining_days <= 0:
                break

            book_ids = [book.id for book in library.books]
            output.append((library.id, book_ids))
            scanned_books.update(book_ids)
            used_libraries.append(unused_libraries.pop(unused_libraries.index(library)))

            break  # break after 1 library and then calculate max score again

    return output


def strategy_7(problem):
    """
    optimal for D (all same value, all same signup time, all same scanned per day)
    number of books is different per library (min 1, max 14)
    220k books, only 79k unique
    every book occurs exactly twice or thrice on the data set
    goal here is to add as many unique books every time
    just calculate the score (=number of books not added yet) per library and sort on that

    Total: 5,028,790 (98.43%) of 5,109,000. optimal or very close to optimal
    """

    output = list()
    remaining_days = problem.n_days

    unused_libraries = problem.libraries.copy()
    used_libraries = list()
    scanned_books = set()

    while remaining_days > 0:

        print(len(scanned_books))  # last print is 77366, but starts quickly and later only adds 1
        if len(scanned_books) >= 3000:
            break

        max_score_libraries = np.array(calc_max_score_library(unused_libraries, scanned_books))

        for _, library in sorted(zip(max_score_libraries, unused_libraries), reverse=True):
            remaining_days = remaining_days - library.signup_time
            if remaining_days <= 0:
                break

            book_ids = [book.id for book in library.books if book.id not in scanned_books]
            output.append((library.id, book_ids))
            scanned_books.update(book_ids)
            used_libraries.append(unused_libraries.pop(unused_libraries.index(library)))

            break  # break after 1 library and then calculate max score again

    return output


def strategy_7_fast(problem):
    """
    optimal for D (all same value, all same signup time, all same scanned per day)
    number of books is different per library (min 1, max 14)
    220k books, only 79k unique
    every book occurs exactly twice or thrice on the data set
    goal here is to add as many unique books every time
    just calculate the score (=number of books not added yet) per library and sort on that

    Total: 5,028,790 (98.43%) of 5,109,000. optimal or very close to optimal
    """

    output = [None] * 15000
    remaining_days = problem.n_days
    unused_libraries = problem.libraries.copy()
    scanned_books = set()

    library_i = 0
    while remaining_days > 0:

        # print(library_i, len(scanned_books))  # last print is 77366, but starts quickly and later only adds 1
        # if len(scanned_books) >= 3000:
        #     break

        max_score_libraries = calc_max_score_library_fast(unused_libraries, scanned_books)
        max_index = max_score_libraries.index(max(max_score_libraries))

        library = unused_libraries.pop(max_index)

        remaining_days -= library.signup_time
        if remaining_days <= 0:
            break

        book_ids = library.book_ids - scanned_books
        output[library_i] = (library.id, tuple(book_ids))
        scanned_books.update(book_ids)
        library_i += 1

    return output[:library_i]


def strategy_7_fast2(problem):
    """
    optimal for D (all same value, all same signup time, all same scanned per day)
    number of books is different per library (min 1, max 14)
    220k books, only 79k unique
    every book occurs exactly twice or thrice on the data set
    goal here is to add as many unique books every time
    just calculate the score (=number of books not added yet) per library and sort on that

    Total: 5,028,790 (98.43%) of 5,109,000. optimal or very close to optimal
    """

    output = [(0, ())] * 15000
    remaining_days = problem.n_days
    unused_libraries = problem.libraries.copy()
    scanned_books = set()
    library_i = 0

    stop = False
    while not stop:

        # print(library_i, len(scanned_books))  # last print is 77366, but starts quickly and later only adds 1
        # if len(scanned_books) >= 2000:
        #     break

        max_score_libraries = calc_max_score_library_fast4(unused_libraries, scanned_books)
        recent_new_book_ids = set()
        while not stop:
            max_index = max_score_libraries.index(max(max_score_libraries))
            len_book_ids, book_ids = max_score_libraries.pop(max_index)

            if len(book_ids - recent_new_book_ids) != len_book_ids:
                break

            library = unused_libraries.pop(max_index)

            remaining_days -= library.signup_time
            if remaining_days <= 0:
                stop = True
                break

            output[library_i] = (library.id, tuple(book_ids))
            scanned_books.update(book_ids)
            recent_new_book_ids.update(book_ids)
            library_i += 1

    return output[:library_i]


def strategy_7_fast3(problem, output=None):
    """
    optimal for D (all same value, all same signup time, all same scanned per day)
    number of books is different per library (min 1, max 14)
    220k books, only 79k unique
    every book occurs exactly twice or thrice on the data set
    goal here is to add as many unique books every time
    just calculate the score (=number of books not added yet) per library and sort on that

    Total: 5,033,600 (98.52%) of 5,109,000. optimal or very close to optimal
    """
    # if output is not None:
    #     limit = 10000 + len(output) * 10
    # else:
    #     limit = 10000

    if output is None:
        output = [0, ()] * 15000
        remaining_days = problem.n_days
        unused_libraries = problem.libraries.copy()
        scanned_books = set()
        library_i = 0
    else:
        library_ids = [library_id for library_id, _ in output]
        remaining_days = problem.n_days - sum([problem.libraries[library_id].signup_time for library_id in library_ids])
        unused_libraries = [library for library in problem.libraries.copy() if library.id not in library_ids]
        output = [(library_id, problem.libraries[library_id].book_ids) for library_id in library_ids]
        scanned_books = set(itertools.chain.from_iterable([book_ids for _, book_ids in output]))
        output += [0, ()] * (15000 - len(output))
        library_i = len(library_ids)

    # print(limit, library_i)

    stop = False
    while not stop:

        # print(library_i, len(scanned_books))  # last print is 77366, but starts quickly and later only adds 1
        # if len(scanned_books) >= 10000:
        #     break

        max_score_libraries = calc_max_score_library_fast4(unused_libraries, scanned_books)
        recent_new_book_ids = set()
        while not stop:
            max_index = max_score_libraries.index(max(max_score_libraries))
            len_book_ids, new_book_ids = max_score_libraries.pop(max_index)

            if len(new_book_ids - recent_new_book_ids) != len_book_ids:
                break

            library = unused_libraries.pop(max_index)
            book_ids = library.book_ids  # add all books of library, not just the uniques

            remaining_days -= library.signup_time
            if remaining_days <= 0:
                stop = True
                break

            output[library_i] = (library.id, tuple(book_ids))
            scanned_books.update(book_ids)
            recent_new_book_ids.update(new_book_ids)
            library_i += 1

    return output[:library_i]


def strategy_8(problem):
    """
    optimal for D (all same value, all same signup time, all same scanned per day)
    number of books is different per library (min 1, max 14)
    220k books, only 79k unique
    every book occurs exactly twice or thrice on the data set
    goal here is to add as many unique books every time
    just calculate the score (=number of books not added yet) per library and sort on that

    same thinking as 7, but different implementation.
    start with all libraries, remove libraries that decrease unique books least when they are removed
    too slow
    """

    output = list()
    remaining_days = problem.n_days

    used_libraries = problem.libraries.copy()

    for i in range(15000):
        print(i)
        least_loss = 20
        for library_i, library in enumerate(used_libraries):
            all_book_ids = {book.id for library in used_libraries for book in library.books}
            other_libraries = used_libraries[:library_i] + used_libraries[library_i+1:]
            book_ids_others = {book.id for library in other_libraries for book in library.books}
            loss = len(all_book_ids) - len(book_ids_others)
            if loss == 0:
                remove_index = used_libraries.index(library)
                least_loss = 0
                break
            elif loss < least_loss:
                least_loss = loss
                remove_index = used_libraries.index(library)
        print(least_loss)
        used_libraries.pop(remove_index)

    return output


def strategy_9(problem):
    """another attempt to speed up for D
    TOO SLOW"""

    split = 15000
    used_book_ids = [[book.id for book in library.books] for library in problem.libraries[:split]]
    unused_book_ids = [[book.id for book in library.books] for library in problem.libraries[split:]]

    print(len(set(itertools.chain.from_iterable(used_book_ids))))
    print(len(set(itertools.chain.from_iterable(unused_book_ids))))

    for i in range(split):
        print(i)
        best_trial_unique_count = len(set(itertools.chain.from_iterable(used_book_ids)))
        best_trial_index = None
        for j in range(split):
            trial = used_book_ids[:i] + used_book_ids[i+1:] + unused_book_ids[j:j+1]
            trial_unique_count = len(set(itertools.chain.from_iterable(trial)))
            if trial_unique_count > best_trial_unique_count:
                best_trial_unique_count = trial_unique_count
                best_trial_index = j

        if best_trial_index is not None:
            used_book_ids[i], unused_book_ids[best_trial_index] = unused_book_ids[best_trial_index], used_book_ids[i]

        print(len(set(itertools.chain.from_iterable(used_book_ids))))

    output = list()

    return output


def strategy_10(problem):
    """another attempt to speed up for D"""

    output = list()

    rows = 15000
    cols = 14
    np_used_book_ids = np.ones((rows, cols), dtype=int) * -1
    np_unused_book_ids = np.ones_like(np_used_book_ids) * -1

    # init
    for library_i, library in enumerate(problem.libraries):
        book_ids = [book.id for book in library.books]
        if library_i < rows:
            np_used_book_ids[library_i, :len(book_ids)] = np.array(book_ids)
        else:
            np_unused_book_ids[library_i-rows, :len(book_ids)] = np.array(book_ids)

    for i in range(rows):
        copy = np_used_book_ids.copy()
        unique_count = len(np.unique(copy))
        print(i, unique_count)
        for j in range(rows):
            copy[i, :] = np_unused_book_ids[j, :]
            if len(np.unique(copy)) > unique_count:
                np_unused_book_ids[j, :] = np_used_book_ids[i, :]
                np_used_book_ids = copy
                break

    # print(np_unused_book_ids[:10])
    # print(len(np.unique(np_unused_book_ids)) - 1)

    return output


def strategy_11(problem):
    """
    try optimal for E
    short simulation time: 200 days
    varying signup time (1 to 10)
    varying book value (1 to 250)
    varying occurences of books between 1 and 18
    books scanned per day is either 1 or 2
    many libraries cannot scan all their books (too many books, too little time)
    balance maximal possible score within simulation time, with signup time.
    """
    output = list()
    remaining_days = problem.n_days

    max_score_libraries = np.array(calc_total_score_per_library(problem))
    signup_time_libraries = np.array([library.signup_time for library in problem.libraries])
    for _, library in sorted(zip(max_score_libraries / signup_time_libraries, problem.libraries), reverse=True):
        remaining_days = remaining_days - library.signup_time
        if remaining_days <= 0:
            break

        book_ids = [book.id for book in library.books]
        output.append((library.id, book_ids))
    return output


def strategy_12(problem):
    """
    try optimal for E
    short simulation time: 200 days
    varying signup time (1 to 10)
    varying book value (1 to 250)
    varying occurences of books between 1 and 18
    books scanned per day is either 1 or 2
    many libraries cannot scan all their books (too many books, too little time)
    balance maximal possible score within simulation time, with signup time.
    """
    output = list()
    remaining_days = problem.n_days
    scanned_books = set()

    max_score_libraries = np.array(calc_total_score_per_library(problem))
    signup_time_libraries = np.array([library.signup_time for library in problem.libraries])
    for _, library in sorted(zip(max_score_libraries / signup_time_libraries, problem.libraries), reverse=True):
        remaining_days = remaining_days - library.signup_time
        if remaining_days <= 0:
            break

        book_ids = [book.id for book in sorted(library.books, key=lambda x: x.score, reverse=True)
                    if book.id not in scanned_books]

        max_possible_books_to_scan = remaining_days * library.scanned_daily
        book_ids = book_ids[:max_possible_books_to_scan]
        if len(book_ids) <= 0:
            continue

        output.append((library.id, book_ids))
        scanned_books.update(book_ids)
    return output


def strategy_13(problem):
    """
    try optimal for E
    short simulation time: 200 days
    varying signup time (1 to 10)
    varying book value (1 to 250)
    varying occurences of books between 1 and 18
    books scanned per day is either 1 or 2
    many libraries cannot scan all their books (too many books, too little time)
    balance maximal possible score within simulation time, with signup time.
    recalculate the best library to add every step. due to adding books and less days this changes.

    todo: start with the lasts. right now the libraries that appear good at the start may not be so good in the end
    todo: because the books that appear to be worth a lot, may be added later cheaper and duplicates dont count
    """
    output = list()
    remaining_days = problem.n_days
    unused_libraries = problem.libraries.copy()
    scanned_books = set()

    while True:
        max_score_libraries = calc_max_total_score_libraries(unused_libraries, scanned_books, remaining_days)
        signup_time_libraries = [library.signup_time for library in unused_libraries]
        ratio = [x/y for x, y in zip(max_score_libraries, signup_time_libraries)]

        max_index = ratio.index(max(ratio))
        library = unused_libraries.pop(max_index)

        remaining_days = remaining_days - library.signup_time
        if remaining_days <= 0:
            break

        book_ids = [book.id for book in sorted(library.books, key=lambda x: x.score, reverse=True)
                    if book.id not in scanned_books]

        max_possible_books_to_scan = remaining_days * library.scanned_daily
        book_ids = book_ids[:max_possible_books_to_scan]
        if len(book_ids) <= 0:
            continue

        output.append((library.id, book_ids))
        scanned_books.update(book_ids)
    return output


# def strategy_2(problem):
#     """
#     sort libraries on total value that can be achieved within simulation time
#     sort books on value
#     """
#     output = list()
#     max_score_library = calc_total_score_per_library(problem)
#
#     sorted_libraries = [library for _, (_, library) in sorted(zip(max_score_library, enumerate(problem.libraries)), reverse=True)]
#
#     for library_i, library in enumerate(sorted_libraries):
#         output.append((library.id, []))
#         for book_i, book in enumerate(sorted(library.books, key=lambda x: x.score, reverse=True)):
#             output[library_i][1].append(book.id)
#     return output
#
#
# def strategy_3(problem):
#     """
#     sort books on value
#     sort libraries on ascending ratio signup time / total shipping time
#     """
#     output = list()
#     time_ratios_library = calc_ratio_signup_shipping_per_library(problem)
#
#     sorted_libraries = [library for _, (_, library) in sorted(zip(time_ratios_library, enumerate(problem.libraries)))]
#
#     for library_i, library in enumerate(sorted_libraries):
#         output.append((library.id, []))
#         for book_i, book in enumerate(sorted(library.books, key=lambda x: x.score, reverse=True)):
#             output[library_i][1].append(book.id)
#     return output
#
#
# def strategy_4(problem):
#     """
#     sort libraries on ascending ratio signup time / total shipping time
#     sort books on value
#     put unique books first
#     """
#
#     # get all books
#     all_books = []
#
#     for library in problem.libraries:
#         library_book_ids = [book.id for book in library.books]
#         all_books.extend(library_book_ids)
#
#     books_counter = Counter(all_books)
#
#     output = list()
#     time_ratios_library = calc_ratio_signup_shipping_per_library(problem)
#
#     sorted_libraries = [library for _, (_, library) in sorted(zip(time_ratios_library, enumerate(problem.libraries)))]
#
#
#     for library_i, library in enumerate(sorted_libraries):
#         output.append((library.id, []))
#         library_books = library.books
#
#         library_unique_books = [book for book in library.books if books_counter[book.id] == 1]
#         library_non_unique_books = [book for book in library_books if not book in library_unique_books]
#
#         for book_i, book in enumerate(sorted(library_unique_books, key=lambda x: x.score, reverse=True)):
#             output[library_i][1].append(book.id)
#
#         for book_i, book in enumerate(sorted(library_non_unique_books, key=lambda x: x.score, reverse=True)):
#             output[library_i][1].append(book.id)
#
#     return output
#
#
# def strategy_5():
#     """
#     sort libraries on total value that can be achieved within simulation time
#     sort books on value
#     start with a libraries that have short signup, and slow shipping time
#
#     """
#
#     pass
#
#
#
#
#
#
# def strategy_6(problem):
#     """
#     sort libraries on ascending signup time
#     sort books on value
#     """
#     output = list()
#     signup_times_library = calc_signup_time_per_library(problem)
#
#     sorted_libraries = [library for _, (_, library) in sorted(zip(signup_times_library, enumerate(problem.libraries)))]
#
#     for library_i, library in enumerate(sorted_libraries):
#         output.append((library.id, []))
#         for book_i, book in enumerate(sorted(library.books, key=lambda x: x.score, reverse=True)):
#             output[library_i][1].append(book.id)
#     return output
#
#
#
# def strategy_7(problem):
#     """
#     sort libraries on ascending ratio max possible total score / signup time
#     sort books on value
#     """
#     output = list()
#     #signup_times_library = calc_signup_time_per_library(problem)
#
#     ratios_library = calc_total_signup_ratio_per_library(problem)
#
#     sorted_libraries = [library for _, (_, library) in sorted(zip(ratios_library, enumerate(problem.libraries)), reverse=True)]
#
#     for library_i, library in enumerate(sorted_libraries):
#         output.append((library.id, []))
#         for book_i, book in enumerate(sorted(library.books, key=lambda x: x.score, reverse=True)):
#             output[library_i][1].append(book.id)
#     return output
#
#
#
# def strategy_8(problem):
#     """
#     sort libraries on total value that can be achieved within simulation time
#     sort books on value
#     prevent non-unique books
#     """
#     output = list()
#     max_score_library = calc_total_score_per_library(problem)
#
#     books = set()
#
#     sorted_libraries = [library for _, (_, library) in sorted(zip(max_score_library, enumerate(problem.libraries)), reverse=True)]
#
#     for library_i, library in enumerate(sorted_libraries):
#         output.append((library.id, []))
#         for book_i, book in enumerate(sorted(library.books, key=lambda x: x.score, reverse=True)):
#             if book.id in books:
#                 continue
#             output[library_i][1].append(book.id)
#             books.add(book.id)
#         if len(output[library_i][1]) == 0:
#             output[library_i][1].append(book.id)  # to prevent empty lines
#     return output
#
#
# def strategy_9(problem):
#     """
#     sort libraries on ascending ratio max possible total score / signup time
#     sort books on value
#     """
#     output = list()
#     #signup_times_library = calc_signup_time_per_library(problem)
#     books = set()
#
#     ratios_library = calc_total_signup_ratio_per_library(problem)
#
#     sorted_libraries = [library for _, (_, library) in sorted(zip(ratios_library, enumerate(problem.libraries)), reverse=True)]
#
#     for library_i, library in enumerate(sorted_libraries):
#         output.append((library.id, []))
#         for book_i, book in enumerate(sorted(library.books, key=lambda x: x.score, reverse=True)):
#             if book.id in books:
#                 continue
#             output[library_i][1].append(book.id)
#             books.add(book.id)
#         if len(output[library_i][1]) == 0:
#             output[library_i][1].append(book.id)  # to prevent empty lines
#     return output
#
#
# def strategy_10(problem):
#     """
#     sort libraries on ascending ratio max possible total score / signup time
#     sort books on value
#     """
#     output = list()
#     books = set()
#
#     ratios_library = calc_total_signup_ratio_per_library(problem)
#
#     remaining_days = problem.scanning_days
#
#     sorted_libraries = [library for _, (_, library) in sorted(zip(ratios_library, enumerate(problem.libraries)), reverse=True)]
#
#     for library_i, library in enumerate(sorted_libraries):
#         remaining_days = remaining_days - library.signup_time
#         if remaining_days < 0:
#             break
#
#         output.append((library.id, []))
#         max_possible_books_to_scan = remaining_days * library.scanned_daily
#         added_books = 0
#         for book_i, book in enumerate(sorted(library.books, key=lambda x: x.score, reverse=True)):
#             if book.id in books:
#                 continue
#
#             output[library_i][1].append(book.id)
#             books.add(book.id)
#             added_books += 1
#             if added_books == max_possible_books_to_scan:
#                 break
#
#         if len(output[library_i][1]) == 0:
#             output[library_i][1].append(book.id)  # to prevent empty lines
#     return output
#
#
# def strategy_11(problem):
#     """
#     sort libraries on ascending ratio max possible total score / signup time
#     sort books on value
#     """
#     output = list()
#     books = set()
#
#     max_score_library = calc_total_score_per_library(problem)
#
#     remaining_days = problem.scanning_days
#
#     sorted_libraries = [library for _, (_, library) in sorted(zip(max_score_library, enumerate(problem.libraries)), reverse=True)]
#
#     for library_i, library in enumerate(sorted_libraries):
#         remaining_days = remaining_days - library.signup_time
#         if remaining_days < 0:
#             break
#
#         output.append((library.id, []))
#         max_possible_books_to_scan = remaining_days * library.scanned_daily
#         added_books = 0
#         for book_i, book in enumerate(sorted(library.books, key=lambda x: x.score, reverse=True)):
#             if book.id in books:
#                 continue
#
#             output[library_i][1].append(book.id)
#             books.add(book.id)
#             added_books += 1
#             if added_books == max_possible_books_to_scan:
#                 break
#
#         if len(output[library_i][1]) == 0:
#             output[library_i][1].append(book.id)  # to prevent empty lines
#     return output


def main():

    total = 0
    total_max = 0
    for file_i, file in enumerate(files[3:4]):

        file_out = 'out_' + file

        problem = helper.load_input_file(file)

        # output = strategy_0(problem)  # 10,495,004
        # output = strategy_1(problem)  # 10,750,360
        # output = strategy_2(problem)  # 21,465,662 optimal for B
        # output = strategy_3(problem)  # 22,010,334
        # output = strategy_4(problem)  # 22,092,944
        # output = strategy_5(problem)  # 24,160,525
        # output = strategy_6(problem)  # 5,689,822 for C (optimal or very close to optimal)
        # output = strategy_7(problem)  # 5,028,790 for D (optimal or very close) runs slowly!!
        # output = strategy_7_fast(problem)  # 5,028,790 for D (optimal or very close)
        # output = strategy_8(problem)  #
        # output = strategy_9(problem)
        # output = strategy_10(problem)
        # output = strategy_11(problem)  # 3,096,617 (24.68%) of 12,548,648
        # output = strategy_12(problem)  # Total: 5,020,083 (40.00%) of 12,548,648
        # output = strategy_13(problem)  #

        # analyse_output(output)
        # analyse_output2(output, problem) # for C


        output = None
        while True:
            output = strategy_7_fast3(problem, output=output)  # 5,033,600 for D (optimal or very close)
            optimal, output = analyse_output4(output, problem)
            if optimal:
                break


        result = helper.score(file, None, output)
        max_result = calc_max_score(problem)

        total += result
        total_max += max_result

        print('{}: {:,} ({:.2f}%) {:,}\n'.format(file_i, result, 100*result/max_result, max_result))

        helper.create_submission_file(output, file_out)

    print('Total: {:,} ({:.2f}%) of {:,} '.format(total, 100*total/total_max, total_max))


def analyse_output(output):
    n_books = 0
    unique_books = set()

    for library_id, book_ids in output:
        n_books += len(book_ids)
        unique_books.update(book_ids)

    print(f'{n_books} books submitted of which {len(unique_books)} unique ({100*len(unique_books)/n_books:.1f}%)')


def analyse_output2(output, problem):
    ratios = np.zeros(len(output))
    used_library_ids = np.zeros(len(output))
    used_book_ids = set(itertools.chain.from_iterable([ids for _, ids in output]))
    for i, (library_id, book_ids) in enumerate(output):
        used_library_ids[i] = library_id
        others = output[:i] + output[i+1:]
        other_book_ids = set(itertools.chain.from_iterable([ids for _, ids in others]))
        score = sum([problem.book_scores[book_id] if book_id not in other_book_ids else 0 for book_id in book_ids])
        signup_time = problem.libraries[library_id].signup_time
        ratios[i] = score/signup_time

    plt.figure()
    plt.plot(ratios)
    plt.show()

    unused_libraries = [library for j, library in enumerate(problem.libraries) if j not in used_library_ids]
    max_score_libraries = np.array(calc_max_score_library(unused_libraries, used_book_ids))
    signup_time_libraries = np.array([library.signup_time for library in unused_libraries])
    ratios2 = np.sort(max_score_libraries / signup_time_libraries)[::-1]

    plt.figure()
    plt.plot(ratios2)
    plt.show()


def analyse_output3(output, problem):
    all_losses = list()
    remove = list()
    all_book_ids = [problem.libraries[library_id].book_ids for library_id, _ in output]
    set_all_book_ids = set(itertools.chain.from_iterable(all_book_ids))
    for i, (library_id, _) in enumerate(output):
        other_book_ids = set(itertools.chain.from_iterable(all_book_ids[:i] + all_book_ids[i+1:]))
        loss = len(set_all_book_ids - other_book_ids)
        if loss == 0:
            remove.append(i)
        all_losses.append(loss)

    plt.figure()
    plt.plot(all_losses)
    plt.show()

    for i in remove[::-1]:
        del output[i]

    return len(remove) == 0, output


def analyse_output4(output, problem):
    all_book_ids = [problem.libraries[library_id].book_ids for library_id, _ in output]
    counter = Counter(itertools.chain.from_iterable(all_book_ids))

    all_losses = [sum([1 if counter[book_id] == 1 else 0 for book_id in book_ids]) for i, (_, book_ids) in enumerate(output)]
    remove = [i for i, loss in enumerate(all_losses) if loss == 0]

    plt.figure()
    plt.plot(all_losses)
    plt.show()

    for i in remove[::-1]:
        del output[i]
        del all_losses[i]

    # order from most unique to least unique, and remove duplicate books, so that last few libraries are used optimally
    output = [output for _, output in sorted(zip(all_losses, output), reverse=True)]
    unique_book_ids = set()
    output_copy = output.copy()
    for i, (library_id, book_ids) in enumerate(output_copy):
        output[i] = (library_id, tuple(set(book_ids) - unique_book_ids))
        unique_book_ids.update(book_ids)

    return len(remove) == 0, output


def calc_max_score(problem):
    return sum(problem.book_scores)


def calc_max_score_library(libraries, book_ids=None):
    if book_ids is None:
        book_ids = []
    return [sum([book.score if book.id not in book_ids else 0 for book in library.books]) for library in libraries]


def calc_max_score_library_fast(libraries, book_ids):
    """shortcuts: assume score is equal so only length matters"""
    return [len(library.book_ids - book_ids) for library in libraries]


def calc_max_score_library_fast2(libraries, book_ids):
    """shortcuts: assume score is equal so only length matters"""
    return [(len(library.book_ids - book_ids), library.book_ids - book_ids) for library in libraries]


def calc_max_score_library_fast3(libraries, book_ids):
    """shortcuts: assume score is equal so only length matters"""
    out = [(0, 0)] * len(libraries)
    for library_i, library in enumerate(libraries):
        temp = library.book_ids - book_ids
        out[library_i] = (len(temp), temp)
    return out


def calc_max_score_library_fast4(libraries, book_ids):
    """
    shortcuts: assume score is equal so only length matters
    20% faster than calc_max_score_library_fast2
    """
    temp = [library.book_ids - book_ids for library in libraries]
    return list(zip(map(len, temp), temp))


def calc_max_score_library_fast5(libraries, book_ids):
    """
    shortcuts: assume score is equal so only length matters
    20% faster than calc_max_score_library_fast2
    slightly slower than calc_max_score_library_fast4
    """
    temp = list(map(lambda library: library.book_ids - book_ids, libraries))
    return list(zip(map(len, temp), temp))


def calc_unique_books_libraries(libraries):
    book_id_counts = Counter(itertools.chain.from_iterable([[book.id for book in library.books] for library in libraries]))
    unique_books = np.zeros(len(libraries))
    for library_i, library in enumerate(libraries):
        for book in library.books:
            if book_id_counts[book.id] == 2:
                unique_books[library_i] += 1
    # print(book_id_counts)
    return unique_books


def calc_total_score_per_library(problem):
    remaining_days = problem.n_days
    max_score_library = list()
    for library in problem.libraries:
        max_possible_scan_time = remaining_days - library.signup_time
        max_possible_books_to_scan = max_possible_scan_time * library.scanned_daily
        sorted_book_scores = sorted([book.score for book in library.books], reverse=True)
        max_score_library.append(sum(sorted_book_scores[:max_possible_books_to_scan]))

    return max_score_library


def calc_max_total_score_libraries(libraries, book_ids, remaining_days):
    max_total_scores = list()
    for library in libraries:
        max_possible_scan_time = remaining_days - library.signup_time
        max_possible_books_to_scan = max_possible_scan_time * library.scanned_daily
        book_scores = sorted([book.score for book in library.books if book.id not in book_ids], reverse=True)
        max_score_library = sum(book_scores[:max_possible_books_to_scan])
        max_total_scores.append(max_score_library)

    return max_total_scores
#
#
# def calc_signup_time_per_library(problem):
#     """
#     D = number of days
#     D - signup_time
#     """
#     D = problem.scanning_days
#     signup_times = list()
#     for library in problem.libraries:
#         # max_possible_scan_time = D - library.signup_time
#         # max_possible_books_to_scan = max_possible_scan_time * library.scanned_daily
#         # sorted_book_scores = sorted([book.score for book in library.books], reverse=True)
#         # max_score_library.append(sum(sorted_book_scores[:max_possible_books_to_scan]))
#         signup_times.append(library.signup_time)
#
#     return signup_times
#
#
# def calc_ratio_signup_shipping_per_library(problem):
#     D = problem.scanning_days
#     ratio_time_library = list()
#     for library in problem.libraries:
#         # max_possible_scan_time = D - library.signup_time
#         # max_possible_books_to_scan = max_possible_scan_time * library.scanned_daily
#         # sorted_book_scores = sorted([book.score for book in library.books], reverse=True)
#         # max_score_library.append(sum(sorted_book_scores[:max_possible_books_to_scan]))
#         total_shipping_time = library.nr_books / library.scanned_daily
#
#         ratio_signup_shipping = library.signup_time / total_shipping_time
#
#         ratio_time_library.append(ratio_signup_shipping)
#     return ratio_time_library
#
#
# def calc_total_signup_ratio_per_library(problem):
#     D = problem.scanning_days
#     ratio_time_library = list()
#     for library in problem.libraries:
#         max_possible_scan_time = D - library.signup_time
#         max_possible_books_to_scan = max_possible_scan_time * library.scanned_daily
#         sorted_book_scores = sorted([book.score for book in library.books], reverse=True)
#         max_score = sum(sorted_book_scores[:max_possible_books_to_scan])
#
#         signup_time = library.signup_time
#
#         ratio = max_score / signup_time
#
#         ratio_time_library.append(ratio)
#
#     return ratio_time_library


def analyse_1():
    """Distribution of book scores"""

    for file_i, file in enumerate(files):
        problem = helper.load_input_file(file)

        df = pd.DataFrame({'book_scores': problem.book_scores})

        print(df.describe())

        plt.figure()
        df.book_scores.hist(bins=100)
        plt.show()


def analyse_2(file=None):
    """Other statistics"""
    global files

    if file is not None:
        files = [file]

    print(files)
    for file_i, file in enumerate(files):
        problem = helper.load_input_file(file)

        print(f'\nStatistics for file: {file}\n')
        print(pd.DataFrame({problem[:3]}, columns=['n_days', 'n_books', 'n_libraries']))

        print(pd.DataFrame(problem.libraries).describe())
        plt.figure()
        pd.DataFrame(problem.libraries).hist(bins=50)
        plt.show()
        print(pd.DataFrame({'book_scores': problem.book_scores}).describe())

        book_ids = [book.id for library in problem.libraries for book in library.books]
        print(f'Out of {len(book_ids)}, {len(set(book_ids))} are unique')


def analyse_3(file=None):
    """Plot scores per library over time"""

    global files

    if file is not None:
        files = [file]

    for file in files:
        problem = helper.load_input_file(file)

        if file == 'c_incunabula.txt':
            print('too slow for C')
            break

        plt.figure()
        for library in problem.libraries[:1000]:
            remaining_days = problem.n_days - library.signup_time
            max_possible_books_to_scan = remaining_days * library.scanned_daily

            book_scores = [book.score for book in sorted(library.books, key=lambda i: i.score, reverse=True)]
            if len(book_scores) >= max_possible_books_to_scan:
                book_scores_np = np.array(book_scores[:max_possible_books_to_scan])
            else:
                book_scores_np = np.zeros(max_possible_books_to_scan)
                book_scores_np[:len(book_scores)] = book_scores
            book_scores_np = book_scores_np.reshape(remaining_days, library.scanned_daily)

            x = np.arange(library.signup_time, problem.n_days)
            summed_per_day = book_scores_np.sum(axis=1).T

            plt.plot(x, summed_per_day)

        plt.show()


def analyse_b():
    file = 'b_read_on.txt'
    analyse_2(file)

    problem = helper.load_input_file(file)


def analyse_c():
    """analyse c file"""

    file = 'c_incunabula.txt'
    analyse_2(file)

    problem = helper.load_input_file(file)

    book_ids = [book.id for library in problem.libraries for book in library.books]
    counter = Counter(book_ids)
    # print(counter)
    # print(sum(counter.values()))


def analyse_d():
    file = 'd_tough_choices.txt'
    analyse_2(file)

    problem = helper.load_input_file(file)

    book_ids = [book.id for library in problem.libraries for book in library.books]
    counter = Counter(book_ids)

    # print(counter)

    values = list()
    for k, v in counter.items():
        values.append(v)

    print(Counter(values))


    # print(sum(counter.values()))


def analyse_e():
    file = 'e_so_many_books.txt'
    # analyse_2(file)

    problem = helper.load_input_file(file)

    # book_ids = [book.id for library in problem.libraries for book in library.books]
    # counter = Counter(book_ids)

    # print(counter)

    # values = list()
    # for k, v in counter.items():
    #     values.append(v)

    # print(Counter(values))

    # print(sum(counter.values()))

    # analyse_3(file=file)
    # max_total_score_libraries = calc_total_score_per_library(problem)

    solution = helper.load_output_file('out_' + file)
    # print(solution)
    # print(len(solution))
    library_ids = [library_id for library_id, _ in solution]
    scanned_libraries = [problem.libraries[library_id] for library_id in library_ids]
    library_signup_times = [lib.signup_time for lib in scanned_libraries]
    library_scanned_daily = [lib.scanned_daily for lib in scanned_libraries]
    library_max_scores = calc_max_total_score_libraries(scanned_libraries, {}, problem.n_days)

    df = pd.DataFrame(zip(library_ids, library_max_scores, library_signup_times, library_scanned_daily),
                      columns=['id', 'score', 'signup', 'scanned'])

    df['ratio'] = df.score / df.signup
    print(df)
    print(df.describe())


def analyse_f():
    file = 'f_libraries_of_the_world.txt'
    analyse_2(file)

    # problem = helper.load_input_file(file)

    analyse_3(file=file)


def analyse_diff():
    file_out1 = 'out_d_tough_choices.txt'
    file_out2 = 'out_d_tough_choices(1).txt'
    solution1 = helper.load_output_file(file_out1)
    solution2 = helper.load_output_file(file_out2)

    lib1 = {library_id for library_id, book_ids in solution1}
    lib2 = {library_id for library_id, book_ids in solution2}
    book_ids1 = set(itertools.chain.from_iterable([book_ids for library_id, book_ids in solution1]))
    book_ids2 = set(itertools.chain.from_iterable([book_ids for library_id, book_ids in solution2]))
    temp = lib2 - lib1
    # temp2 = book_ids1 - book_ids2
    temp2 = book_ids2 - book_ids1
    print(len(temp), len(book_ids1), len(book_ids2))
    # print(solution1)


def analyse():
    file = 'a_example.txt'
    # file = 'b_read_on.txt'

    files = ['a_example.txt', 'b_read_on.txt', 'c_incunabula.txt', 'd_tough_choices.txt', 'e_so_many_books.txt',
             'f_libraries_of_the_world.txt']

    for file_i, file in enumerate(files):

        problem = helper.load_input_file(file)

        # max_score_library = calc_total_score_per_library(problem)

        # print([j for _, j in sorted(zip(max_score_library, problem.libraries), reverse=True)])
        # # print(max_score_library)


if __name__ == '__main__':
    files = ['a_example.txt', 'b_read_on.txt', 'c_incunabula.txt', 'd_tough_choices.txt', 'e_so_many_books.txt',
             'f_libraries_of_the_world.txt']

    main()
    # analyse()
    # analyse_1()
    # analyse_2()
    # analyse_3()
    # analyse_b()
    # analyse_c()
    # analyse_d()
    # analyse_diff()
    # analyse_e()
    # analyse_f()
