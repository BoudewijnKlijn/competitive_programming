def sort_number(number, reverse):
    return int(''.join(sorted([c for c in str(number)], reverse=reverse)))


def is_increasing(number):
    return sort_number(number, reverse=False) == number


def is_decreasing(number):
    return sort_number(number, reverse=True) == number


def is_bouncy(number):
    return not is_decreasing(number) and not is_increasing(number)


def main():

    bouncy_count = 0
    i = 0

    while True:

        i += 1

        if is_bouncy(i):
            bouncy_count += 1

        # # logging
        # if i % 100000 == 0:
        #     print(i, bouncy_count / i)

        if bouncy_count * 100 == i * 99:
            break

    print(f"Answer: {i}")


if __name__ == '__main__':
    main()
