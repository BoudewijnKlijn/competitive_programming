def create_primes(max):
	for candidate in range(primes[-1]+2,max,2):
		for divisor in primes:
			if(candidate%divisor==0):
				break
			if(divisor*divisor>candidate):
				primes.append(candidate)
				break
				
global primes
limit = 10**7
primes = [2,3]
create_primes(2*int(limit**0.5))