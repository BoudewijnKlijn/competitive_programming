def get_primes_up_to_n(n: int) -> list:
    primes = [2, 3]
    for num in range(5, n + 1, 2):
        for p in primes:
            if num % p == 0:
                break
        else:
            primes.append(num)
    return primes


def get_divisors(n: int) -> list:
    divisors = []
    for p in primes:
        while n % p == 0:
            divisors.append(p)
            n //= p
    return divisors


class Solution:

    primes = get_primes_up_to_n(1000)

    def minSteps(self, n: int) -> int:
        """If n is prime, the only way to get to that number is copying and pasting n times.
        If n is a power of 2, then we can copy and paste each time."""
        if n == 1:
            return 0
        elif n in self.primes:
            return n
        for p in self.primes:
            if n % p == 0:
                return p + self.minSteps(n // p)


primes = get_primes_up_to_n(1000)
print(primes)
for n in range(1, 30):
    print(n, get_divisors(n), Solution().minSteps(n))
