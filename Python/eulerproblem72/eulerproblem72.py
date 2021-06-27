import time
import math
start = time.time()

def create_primes(max):
	for candidate in range(primes[-1]+2,max,2):
		for divisor in primes:
			if(candidate%divisor==0):
				break
			if(divisor*divisor>candidate):
				primes.append(candidate)
				break
				
def find_prime_divisors(d):
	phi = 1
	for divisor in primes:
		k = 0
		if(d%divisor==0):		
			while(d%divisor==0):
				d = d/divisor
				k += 1
			phi = phi*(divisor**(k-1))*(divisor-1)
		if(d==1):
			return phi
	return phi*(d-1)
				
global primes
primes = [2,3]
limit = 10**6
create_primes(math.ceil(limit**0.5))
	
answer = 0
for d in range(2,limit+1):
	answer += find_prime_divisors(d)

print("Answer: ",answer)
end = time.time()
print("Time: ",end-start)