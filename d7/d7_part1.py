import time


def read_file(filename):
    with open(filename, 'r') as f:
        return f.read().split('\n')


def get_prerequisites(contents):
    prerequisites = dict()
    for line in contents:
        step = line[-12]
        prerequisite = line[5]
        if prerequisites.get(step):
            prerequisites[step] += prerequisite
        else:
            prerequisites[step] = [prerequisite]

        if not prerequisites.get(prerequisite):
            prerequisites[prerequisite] = []

    return prerequisites


def main():
    contents = read_file('input.txt')[:-1]
    prerequisites = get_prerequisites(contents)

    executed = set()
    order = ''
    while not all([step in executed for step in prerequisites]):
        possible_to_execute = [step for step, prerequisite in prerequisites.items()
                               if all([p in executed for p in prerequisite])
                               and step not in executed]
        possible_to_execute.sort()
        executed.add(possible_to_execute[0])
        order += possible_to_execute[0]

    answer = order
    print(f"Answer: {answer}")


if __name__ == "__main__":
    start_time = time.time()
    main()
    execution_time = time.time() - start_time
    print("Execution time: {:.5f}s".format(execution_time))
