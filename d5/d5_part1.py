import time


def read_file(filename):
    with open(filename, 'r') as f:
        return f.read()


def same_type(char1, char2):
    return char1.lower() == char2.lower()


def opposite_polarity(char1, char2):
    return char1.isupper() != char2.isupper()


def react(polymer):
    position = 0
    while position < len(polymer) - 1:
        if position < 0:
            position = 0

        char1 = polymer[position]
        char2 = polymer[position + 1]
        if same_type(char1, char2) and opposite_polarity(char1, char2):
            polymer = polymer[0:position] + polymer[position + 2:]
            position -= 1
        else:
            position += 1

    return polymer


def main():
    contents = read_file('input.txt').strip()
    polymer = react(contents)

    answer = len(polymer)
    print(f"Answer: {answer}")


if __name__ == "__main__":
    start_time = time.time()
    main()
    execution_time = time.time() - start_time
    print("Execution time: {:.5f}s".format(execution_time))
