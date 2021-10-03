def read_file(filename):
    with open(filename, 'r') as f:
        return f.read()


def find_duplicate_frequency(integers):
    number_of_integers = len(integers)
    observed_sums = set()
    current_sum = 0
    position = 0
    while current_sum not in observed_sums:
        observed_sums.add(current_sum)

        mod_position = position % number_of_integers
        current_sum += integers[mod_position]

        position += 1

    return current_sum


def main():
    contents = read_file('input.txt')
    integers = [int(c) for c in contents.split()]
    answer = find_duplicate_frequency(integers)

    print(f"Answer: {answer}")


if __name__ == "__main__":
    main()
