from functools import reduce
import pandas as pd


def get_primes(max_number):
    primes = [2]
    for candidate in range(3, max_number, 2):
        add = True
        for prime in primes:
            if candidate % prime == 0:
                add = False
                break
        if add:
            primes.append(candidate)

    return primes


def is_prime(number, primes):
    return number in primes


def get_prime_divisors(number, primes):
    divisors = set()
    for prime in primes:
        while number % prime == 0:
            number = number / prime
            divisors.add(prime)
        if prime > number:
            break
    assert number == 1
    return divisors


def radical(number, primes):
    if number == 1:
        return 1
    return reduce(lambda a, b: a * b, get_prime_divisors(number, primes))


def main():
    n = 100000
    k = 10000
    primes = get_primes(n)
    radicals = [radical(i, primes) for i in range(1, n+1)]
    df = pd.DataFrame({'rad': radicals}, index=range(1, len(radicals)+1))
    df['n'] = df.index
    print(df.sort_values(by=['rad', 'n']).index[k-1])


if __name__ == '__main__':
    main()
