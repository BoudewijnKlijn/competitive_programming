import math

def create_primes(max):
	for candidate in range(primes[-1]+2,max,2):
		for divisor in primes:
			if(candidate%divisor==0):
				break
			if(divisor*divisor>candidate):
				primes.append(candidate)
				break
				
def f_gcd(num_1,num_2):
	gcd, divisor = 1, 2
	while(divisor<=num_1 and divisor<=num_2):
		if(num_1%divisor==0 and num_2%divisor==0):
			gcd = gcd*divisor
			num_1 = num_1/divisor
			num_2 = num_2/divisor
		else: divisor+=1
	return gcd
	
global primes
limit = 10**6
primes = [2,3]
create_primes(limit)

goal=3/7
print(goal)
index=0
while(primes[index]<goal*limit):
	index+=1
num = primes[index-1]
denom = limit
difference = goal - num/denom
print("Num/denom: ",num,denom,num/denom,difference)

# primes in denominator, normal number in numerator
for denom in reversed(primes):
	num = int(denom*goal)
	while(num/denom < goal):
		if(goal-num/denom<difference):
			difference = goal-num/denom
			print("Num/denom: ",num,denom,num/denom,difference)
		num += 1

# primes in numerator, normal number in denominator
for num in primes:
	if(num//goal>limit):
		break
	denom = math.ceil(num/goal)
	while(num/denom < goal):
		if(goal-num/denom<difference):
			difference = goal-num/denom
			print("Num/denom: ",num,denom,num/denom,difference)
		denom -= 1

# normal number in numerator, normal number in denominator
start = math.ceil(goal*limit)
for num in range(start,0,-1):
	for denom in range(limit,1,-1):
		if(num/denom > goal):
			break
		if(goal-num/denom<difference):
			gcd = f_gcd(num,denom)
			if( (gcd>1 and num/gcd!=3) or gcd==1 ):
				difference = goal-num/denom
				print("Num/denom: ",num,denom,num/denom,difference,gcd,num/gcd)	