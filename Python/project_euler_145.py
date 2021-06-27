def reverse(number):
    return int(str(number)[::-1])


def all_odd(number):
    return all([int(c) % 2 == 1 for c in str(number)])


def main():
    reversible_numbers = set()
    max_number = 1000000
    for number in range(1, max_number):
        if str(number)[-1] == '0':
            continue
        elif all_odd(number + reverse(number)):
            reversible_numbers.add(number)
            print(number, reverse(number), number+reverse(number))
    return reversible_numbers


if __name__ == '__main__':
    ans = main()
    print(len(ans))