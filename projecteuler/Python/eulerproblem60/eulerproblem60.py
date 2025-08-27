import time
import sys
start = time.time()

def is_prime(number):
	if(number==2):
		return 1
	for divisor in primes:
		if(number%divisor==0):
			return 0
		if(divisor*divisor>number):
			return 1

def append_primes(new_max):
	for candidate in range(primes[-1]+2,new_max+3,2):
		for divisor in primes:
			if(candidate%divisor==0):
				break
			if(divisor*divisor>candidate):
				primes.append(candidate)
				break

def cat_int(num1,num2):
	return int(str(num1)+str(num2))
	
def is_prime_pair(num1,num2):
	return (is_prime(cat_int(num1,num2))==1 and is_prime(cat_int(num2,num1))==1)

def is_prime_pair_set(prime_set):
	for i in range(len(prime_set)-1,0,-1):
		for j in range(i-1,-1,-1):
			if(is_prime_pair(prime_set[i],prime_set[j])!=1):
				return 0
	return 1

global primes 
primes = [2,3]
append_primes(31628)

prime_set = [0,0,0,0,0]
for index1 in range(0,len(primes)):
	prime_set[0] = primes[index1]
	for index2 in range(0,index1):
		if(is_prime_pair(primes[index1],primes[index2])==1):
			prime_set[1] = primes[index2]
			for index3 in range(0,index2):
				if(is_prime_pair_set(prime_set[:2]+[primes[index3]])==1):
					prime_set[2] = primes[index3]
					for index4 in range(0,index3):
						if(is_prime_pair_set(prime_set[:3]+[primes[index4]])==1):
							prime_set[3] = primes[index4]
							for index5 in range(0,index4):
								if(is_prime_pair_set(prime_set[:4]+[primes[index5]])==1):
									prime_set[4] = primes[index5]
									print("Set: ",prime_set,", Answer: ",sum(prime_set))
									end = time.time()
									print(end-start)
									sys.exit()