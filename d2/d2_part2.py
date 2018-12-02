import time


def read_file(filename):
    with open(filename, 'r') as f:
        return f.read()


def find_similar_box_ids(strings):
    line_items = strings.split()

    for object_position, object1 in enumerate(line_items):
        for object2 in line_items[object_position+1:]:
            differences = 0
            for character_position, character in enumerate(object1):
                if object2[character_position] == character:
                    continue
                else:
                    differences += 1
                    if differences > 1:
                        break

            if differences <= 1:  # assuming just one pair with only one character difference
                return object1, object2


def main():
    contents = read_file('input.txt')
    object1, object2 = find_similar_box_ids(contents)

    print("Answer: ", end="")
    for position, character in enumerate(object1):
        if object2[position] == character:
            print(character, end="")


if __name__ == "__main__":
    start_time = time.time()
    main()
    execution_time = time.time() - start_time
    print("\nExecution time: {:.5f}s".format(execution_time))
