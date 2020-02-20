from collections import namedtuple


def load_file(filename):
    with open(filename, 'r') as f:
        return f.read().strip()


def score(filename_in='sample_in.txt', filename_out='sample_out.txt'):
    contents_in = load_file(filename_in)
    contents_out = load_file(filename_out)

    Settings = namedtuple('Settings', ['B', 'L', 'D'])

    settings = None
    book_scores = None

    for i, line in enumerate(contents_in.split('\n')):
        new = line.split(' ')
        if i == 0:
            settings = Settings(*new)
        elif i == 1:
            book_scores = new
        else:
            pass
            # rides.append(Ride(*new))

        print(settings)

    return settings, book_scores


if __name__ == '__main__':
    score()
