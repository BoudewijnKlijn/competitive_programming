t = 20000
tests = list()


def sum_digits(number: int) -> int:
    return sum([int(i) for i in str(number)])


added = 0
number = 1
while added < t:
    for stop in range(1, number+1):

        if sum_digits(number) < stop:
            break
        tests.append(f'{number} {stop}\n')
        added += 1
    number += 1

with open('in2', 'w') as f:
    f.writelines(tests)
