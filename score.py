from script import load_input_file
from collections import namedtuple


# class Solution:
#     def __init__(self, library_order=None):
#         # list of library ids
#         self.library_order = library_order

def load_output_file(filename):
    # [[library_id, [book_id1, book_id2,...]], ...]
    solution = []

    with open(filename, 'r') as f:
        solution_lines = f.readlines()
        for idx, line in enumerate(solution_lines):
            values = line.split()

            if idx == 0:
                pass
            elif idx % 2 != 0:
                library_id = int(values[0])
            else:
                library_books_shipped = [int(value) for value in values]
                solution.append([library_id, library_books_shipped])

    return solution


def score2(filename_in='sample_in.txt', filename_out='sample_out.txt'):
    problem = load_input_file(filename_in)
    solution = load_output_file(filename_out)

    books = set()

    remaining_days = problem.scanning_days

    while remaining_days > 0 and len(solution) > 0:  # add another library
        library_id, _ = solution.pop(0)
        library = [library for library in problem.libraries if library.id == library_id][0]
        remaining_days = remaining_days - library.signup_time
        max_possible_books_to_scan = remaining_days * library.scanned_daily
        scanned_books = [book.id for book in library.books][:max_possible_books_to_scan]
        books.update(scanned_books)

    score = sum([book_values.score for book_values in problem.books.values() if book_values.id in books])

    return score

# def score(filename_in='sample_in.txt', filename_out='sample_out.txt'):
#     problem = load_input_file(filename_in)
#     solution = load_output_file(filename_out)
#
#     score = 0
#
#     # Library that is currently being signed up
#     signing_up_library_index = 0
#
#     # Number of time steps current sign-up process is ongoing
#     signing_up_duration = 0
#
#     # structure: [(library_id, scanned_per_day), ...]
#     signedup_libraries = []
#
#     scanned_book_ids = []
#
#     for day in range(problem.scanning_days):
#         print('\nDay {} starts'.format(day))
#         for (library_index_in_solution, scanned_per_day) in signedup_libraries:
#             book_ids_scanned_today_for_this_library = solution[library_index_in_solution][1][:scanned_per_day]
#
#             for book_id in book_ids_scanned_today_for_this_library:
#                 if not book_id in scanned_book_ids:
#                     score_increment = problem.books[book_id].score
#
#                     scanned_book_ids.append(book_id)
#                     score += score_increment
#
#                 del solution[library_index_in_solution][1][:scanned_per_day]
#
#             print('Books scanned today for library {}'.format(solution[library_index_in_solution][0]))
#             print(book_ids_scanned_today_for_this_library)
#
#         if signing_up_duration == 0:
#             current_library_id = solution[signing_up_library_index][0]
#             signup_time_current_library = problem.libraries[current_library_id].signup_time
#
#             print('Day {}, start to sign up library {}, will take {} days'.format(day,
#                                                                                   current_library_id,
#                                                                                   signup_time_current_library))
#
#             signing_up_duration += 1
#
#         else:
#             if signing_up_duration == signup_time_current_library:
#                 print('Signup completed for library {}'.format(current_library_id))
#                 signedup_libraries.append(
#                     (signing_up_library_index, problem.libraries[current_library_id].scanned_daily))
#
#                 # If signup time is completed, reset duration and move to next library for signing up
#                 signing_up_duration = 0
#                 signing_up_library_index += 1
#             else:
#                 signing_up_duration += 1
#
#
#     return score


if __name__ == '__main__':
    # file_in = 'c_incunabula.txt'
    # file_out = 'out_c_incunabula.txt'
    # s = score(filename_in=file_in, filename_out=file_out)
    # s = score()

    # file_in = 'f_libraries_of_the_world.txt'
    # file_out = 'out_f_libraries_of_the_world.txt'
    # s = score(filename_in=file_in, filename_out=file_out)

    # file_in = 'b_read_on.txt'
    # file_out = 'out_b_read_on.txt'
    # s = score(filename_in=file_in, filename_out=file_out)

    # file_in = 'a_example.txt'
    # file_out = 'out_a_example.txt'

    file_in = 'd_tough_choices.txt'
    file_out = 'out_d_tough_choices.txt'

    s = score2(filename_in=file_in, filename_out=file_out)

    print(s)
