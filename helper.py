from collections import namedtuple


Problem = namedtuple('Problem', ['n_days', 'n_books', 'n_libraries', 'libraries', 'book_scores'])
Library = namedtuple('Library', ['id', 'signup_time', 'scanned_daily', 'n_books', 'books', 'book_ids'])
Book = namedtuple('Book', ['id', 'score'])


def load_input_file(filename):

    libraries = list()
    library_id = 0

    with open(filename, 'r') as f:
        contents = f.read().strip()
        for line_i, line in enumerate(contents.split('\n')):
            values = [int(x) for x in line.split(' ')]
            if line_i == 0:
                n_books_problem, n_libraries, n_days = values
            elif line_i == 1:
                book_scores = values
            elif line_i % 2 == 0:
                n_books, signup_time, scanned_daily = values
            else:
                books = [Book(id=book_id, score=book_scores[book_id]) for book_id in values]
                book_ids = set(values)
                library = Library(id=library_id, signup_time=signup_time, scanned_daily=scanned_daily, n_books=n_books,
                                  books=books, book_ids=book_ids)
                libraries.append(library)
                library_id += 1

    problem = Problem(n_days=n_days, n_books=n_books_problem, n_libraries=n_libraries,
                      libraries=libraries, book_scores=book_scores)

    return problem


def load_output_file(filename):
    """ output: [[library_id, [book_id1, book_id2,...]], [...]] """

    solution = list()
    with open(filename, 'r') as f:
        contents = f.read().strip()
        for line_i, line in enumerate(contents.split('\n')):
            values = [int(x) for x in line.split(' ')]
            if line_i == 0:
                continue
            elif line_i % 2 != 0:
                library_id, _ = values
            else:
                library_books_shipped = values
                solution.append([library_id, library_books_shipped])

    return solution


def score(filename_in='sample_in.txt', filename_out='sample_out.txt', solution=None):
    problem = load_input_file(filename_in)

    if solution is None:
        solution = load_output_file(filename_out)

    solution_copy = solution.copy()

    library_dict = {i: library for i, library in enumerate(problem.libraries)}

    books = set()
    remaining_days = problem.n_days
    while remaining_days > 0 and len(solution_copy) > 0:
        library_id, book_ids = solution_copy.pop(0)
        library = library_dict[library_id]
        remaining_days = remaining_days - library.signup_time

        if remaining_days < 0:
            break

        max_possible_books_to_scan = remaining_days * library.scanned_daily
        scanned_books = book_ids[:max_possible_books_to_scan]
        books.update(scanned_books)

    score = sum([book_score for book_score_i, book_score in enumerate(problem.book_scores) if book_score_i in books])

    return score


def create_submission_file(output, filename_out='out.txt'):
    with open(filename_out, 'w') as f:
        f.write(f'{len(output)}\n')
        for i, (library_id, books) in enumerate(output):
            f.write(f'{library_id} {len(books)}\n')
            f.write(' '.join([str(book_id) for book_id in books]))

            if i != len(output) - 1:
                f.write('\n')


if __name__ == '__main__':
    file_in = 'a_example.txt'
    file_out = 'out_' + file_in

    problem = load_input_file(file_in)
    # print(problem)
    # print(dir(problem.libraries))

    s = score(filename_in=file_in, filename_out=file_out)
    print(s)
