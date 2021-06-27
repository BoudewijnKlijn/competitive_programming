import time
start = time.time()

def sort_digits(number):
	number_list = [int(x) for x in str(number)]
	digits = len(number_list)
	for i in range(0,digits-1):
		for j in range(0,digits-1):
			if(number_list[j]>number_list[j+1]):
				number_list[j+1], number_list[j] = number_list[j], number_list[j+1]
	return number_list

def phi_value(candidate_1,candidate_2):
	return (candidate_1*candidate_2-candidate_1-candidate_2+1)
	
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

minimum = 1.1
for candidate_1 in reversed(primes):
	for candidate_2 in primes[1:]:
		if(candidate_1*candidate_2>limit):
			break
		else:
			if(sort_digits(candidate_1*candidate_2)==sort_digits(phi_value(candidate_1,candidate_2))):
				frac = candidate_1*candidate_2/int(phi_value(candidate_1,candidate_2))
				if(frac<minimum):
					print("Possible solution: ",candidate_1*candidate_2,", Divisors:",candidate_1,candidate_2,", n/phi(n): ",frac)
					minimum=frac
					
end = time.time()
print("Time: ",end-start)				