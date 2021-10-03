import time
start = time.time()

def last_x_digits(goal_remaining, digits_remaining, minimum_value, total_solutions):
	if(digits_remaining==2):
		return(total_solutions + goal_remaining//2-minimum_value+1)
	while(minimum_value*digits_remaining<=goal_remaining):
		total_solutions = last_x_digits(goal_remaining-minimum_value, digits_remaining-1, minimum_value, total_solutions)
		minimum_value +=1
	return(total_solutions)
		
goal = 100
total_solutions = 0
for digits in range(2,goal+1):
	total_solutions = last_x_digits(goal, digits, 1, total_solutions)
print("Answer: ",total_solutions)

end = time.time()
print("Time: ",end-start)