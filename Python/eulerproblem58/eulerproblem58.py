import time
start = time.time()

def is_prime(number):
	if(number==2):
		return 1
	if(number%2==0): 
		return 0
	divisor = 3
	while(divisor*divisor<=number):
		if(number%divisor==0):
			return 0
		divisor+=2
	return 1
	
number = 1
n_number = 1
n_prime = 0
go = 1
run = 1
while(go):
	for i in range(1,5):
		number += 2*run
		n_number += 1
		n_prime += is_prime(number)
	if(n_prime*10 < n_number):
		go=0
	else:
		run+=1
	
print("Answer: ",run*2+1)

end = time.time()
print("Time: ",end-start)