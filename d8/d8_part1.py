import time

from collections import deque


meta_data_total = 0


def read_file(filename):
    with open(filename, 'r') as f:
        return f.read().split()


def analyze(contents):
    global meta_data_total

    number_of_child_nodes = contents.popleft()
    number_of_metadata_entries = contents.popleft()

    for _ in range(number_of_child_nodes):
        analyze(contents)

    for _ in range(number_of_metadata_entries):
        meta_data_total += contents.popleft()


def main():
    contents = [int(i) for i in read_file('input.txt')]
    contents = deque(contents)

    analyze(contents)

    answer = meta_data_total
    print(f"Answer: {answer}")


if __name__ == "__main__":
    start_time = time.time()
    main()
    execution_time = time.time() - start_time
    print("Execution time: {:.5f}s".format(execution_time))
