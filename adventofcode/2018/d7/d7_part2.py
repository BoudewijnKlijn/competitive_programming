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
    working_on = dict()
    total_time = 0
    while not all([step in executed for step in prerequisites]):

        # Determine which steps can be worked on.
        possible_to_execute = [step for step, prerequisite in prerequisites.items()
                               if all([p in executed for p in prerequisite])
                               and step not in executed
                               and step not in working_on]
        possible_to_execute.sort()

        # Assign steps to the workers
        while len(possible_to_execute) > 0 and len(working_on) < 5:
            work_on_step = possible_to_execute.pop(0)
            working_on[work_on_step] = ord(work_on_step) - 4

        # Execute work here and clear workers when ready.
        delete = []
        for step, time_left in working_on.items():
            working_on[step] = time_left - 1
            if working_on[step] == 0:
                delete.append(step)
                executed.add(step)
        for step in delete:
            del working_on[step]

        # Track working time.
        total_time += 1

    answer = total_time
    print(f"Answer: {answer}")


if __name__ == "__main__":
    start_time = time.time()
    main()
    execution_time = time.time() - start_time
    print("Execution time: {:.5f}s".format(execution_time))
