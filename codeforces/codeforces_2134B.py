import os


def get_primes(n):
    """Get primes up to n."""
    primes = [2, 3]
    for p in range(5, n + 1, 2):
        for prime in primes:
            if p % prime == 0:
                # not prime
                break
        else:
            # prime. not divisable by other primes.
            primes.append(p)
    return primes


primes = get_primes(30)


def solve():
    """We get GCD > 1, if they have at least one common prime factor.
    We can easily achieve this by making all numbers even, if k is odd.
    If n == 1, then we can just do nothing. Output the input, assuming a > 1.
    If k"""
    n, k = list(map(int, input().split()))
    a = list(map(int, input().split()))
    if n == 1:
        # just add k once, to be sure that a becomes > 1.
        print(a[0] + k)
        return

    # n > 1
    if k % 2:
        # k is odd. make all numbers a even.
        for i in range(len(a)):
            if a[i] % 2:
                a[i] += k
        print(" ".join(map(str, a)))
    else:
        # k is even. if all numbers a are even, then we can just output a without adjusting
        # if k is even we need to add k until all have one common prime factor.
        # first find the smallest prime that is not a divisor of k.
        # then add k until that smallest prime is a divisor

        # find smallest prime thats not a divisor
        for p in primes:
            if k % p != 0:
                break

        for i in range(len(a)):
            for _ in range(k):
                if a[i] % p != 0:
                    a[i] += k
                else:
                    break
        print(" ".join(map(str, a)))


if __name__ == "__main__":
    MULTIPLE_TESTS = True

    if not os.path.exists("LOCAL"):
        t = 1
        if MULTIPLE_TESTS:
            t = int(input())

        for _ in range(t):
            solve()
    else:
        import test_runner

        test_runner.main(solve, __file__, MULTIPLE_TESTS)
