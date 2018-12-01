# sum([int(i) for i in open('input.txt').read().split()])


def read_file(filename):
    with open(filename, 'r') as f:
        return f.read()


def main():
    contents = read_file('input.txt')
    integers = [int(c) for c in contents.split()]
    answer = sum(integers)
    print(f"Answer: {answer}")


if __name__ == "__main__":
    main()
