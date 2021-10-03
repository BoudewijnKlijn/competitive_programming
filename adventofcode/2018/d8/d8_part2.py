import time

from collections import deque


def read_file(filename):
    with open(filename, 'r') as f:
        return f.read().split()


def analyze(contents):
    number_of_child_nodes = contents.popleft()
    number_of_metadata_entries = contents.popleft()

    child_node_values = [0] * (number_of_child_nodes + 1)
    for child_node_entry_i in range(number_of_child_nodes):
        child_node_values[child_node_entry_i + 1] = analyze(contents)

    value = 0
    for _ in range(number_of_metadata_entries):
        meta_data_value = contents.popleft()

        if number_of_child_nodes == 0:
            value += meta_data_value
        else:
            try:
                value += child_node_values[meta_data_value]
            except:
                pass

    return value


def main():
    contents = [int(i) for i in read_file('input.txt')]
    contents = deque(contents)

    answer = analyze(contents)
    print(f"Answer: {answer}")


if __name__ == "__main__":
    start_time = time.time()
    main()
    execution_time = time.time() - start_time
    print("Execution time: {:.5f}s".format(execution_time))
