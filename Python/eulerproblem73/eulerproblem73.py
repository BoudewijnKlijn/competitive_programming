import math
import time
start = time.time()

def create_primes(max):
	for candidate in range(primes[-1]+2,max,2):
		for divisor in primes:
			if(candidate%divisor==0):
				break
			if(divisor*divisor>candidate):
				primes.append(candidate)
				break
				
def find_divisors(d):
	for divisor in primes:
		if(divisor>d):
			break
		if(d%divisor==0):
			divisor_list.append(divisor)
			while(d%divisor==0):
				d = d/divisor	

# def find_divisors(d):
	# divisor = 2
	# while(divisor<=d):
		# if(d%divisor==0):
			# divisor_list.append(divisor)
			# while(d%divisor==0):
				# d = d/divisor
		# else:
			# divisor+=1
				
global primes
limit = 12000
primes = [2,3]
create_primes(limit)
	
global divisor_list
answer = 0
for d in range(4,limit+1):
	divisor_list = []
	find_divisors(d)
	for n in range(math.ceil(d/3),math.floor(d/2)+1):
		for divisor in divisor_list:
			if(n%divisor==0):
				break
			elif(divisor>n):
				answer+=1
				break
			elif(divisor==divisor_list[-1]):
				answer+=1

print("Answer: ",answer)
end = time.time()
print("Time: ",end-start)