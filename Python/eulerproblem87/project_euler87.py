import math


def get_primes(up_to: int):
    primes = []
    for candidate in range(2, up_to + 1):
        is_prime = True
        for p in primes:
            if candidate % p == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(candidate)
    return primes


# first create all primes
below = 50*10**6
up_to = math.floor(math.sqrt(below - 2**3 - 2**4))
primes = get_primes(up_to=up_to)
print(f"Number of primes: {len(primes)}")

# then create combinations (but don't check everything
correct = set()
for i in range(len(primes)-1, -1, -1):
    square = primes[i] ** 2
    for j in range(len(primes)):
        cube = primes[j] ** 3
        if square + cube > below:
            break
        for k in range(len(primes)):
            fourth = primes[k] ** 4
            if square + cube + fourth > below:
                break

            candidate = square + cube + fourth
            if candidate < below:
                correct.add(candidate)

print(f"Answer: {len(correct)} combinations below {below}.")
