def sum_square_digits(number):
    return sum(int(c) ** 2 for c in str(number))


def find_stuck_at(number):
    while number != 1 and number != 89:
        number = sum_square_digits(number)
    return number


def generate_sets():
    stuck_at_1 = set()
    stuck_at_89 = set()
    for number in range(1, max_sum_square_digits + 1):
        stuck = find_stuck_at(number)
        if stuck == 1:
            stuck_at_1.add(number)
        elif stuck == 89:
            stuck_at_89.add(number)
        else:
            ValueError
    return stuck_at_1, stuck_at_89


def main():
    stuck_at_1, stuck_at_89 = generate_sets()
    count_1 = 0
    count_89 = 0
    for number in range(1, max_number + 1):
        sum_square = sum_square_digits(number)
        if sum_square in stuck_at_1:
            count_1 += 1
        elif sum_square in stuck_at_89:
            count_89 += 1
        else:
            ValueError

    return count_1, count_89


if __name__ == "__main__":
    max_number = 10 ** 7 - 1
    digits_max_number = len(str(max_number))
    max_sum_square_digits = digits_max_number * 9 ** 2

    count_1, count_89 = main()
