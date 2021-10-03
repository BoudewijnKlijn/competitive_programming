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

def last_x_digits(goal_remaining, digits_remaining, minimum_value, total_solutions):
	if(digits_remaining==1 and minimum_value<=goal_remaining):
		if(goal_remaining in primes):
			return(total_solutions+1)
		else:
			return(total_solutions)
	while(minimum_value*digits_remaining<=goal_remaining):
		total_solutions = last_x_digits(goal_remaining-minimum_value, digits_remaining-1, minimum_value, total_solutions)
		minimum_value = primes[primes.index(minimum_value)+1]
	return(total_solutions)
	
global primes
limit = 100
primes = [2,3]
create_primes(limit)

goal = 2
total_solutions = 0
while(total_solutions<5000):
	total_solutions = 0
	goal += 1
	for digits in range(1,goal+1):
		total_solutions = last_x_digits(goal, digits, primes[0], total_solutions)
		if(total_solutions>5000):
			break
	print("Number: ",goal," in different ways: ",total_solutions)

end = time.time()
print("Time: ",end-start)