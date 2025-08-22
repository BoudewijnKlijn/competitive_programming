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
