import time
start = time.time()

def is_palindrome (number):
	digits = len(str(number))
	for i in range(0,digits//2):
		if str(number)[i] != str(number)[digits-1-i]:
			return 0		
	return 1
	
def reverse (number):
	digits = len(str(number))
	reverse_number = 0
	for i in range(0,digits):
		reverse_number = reverse_number*10 + int(str(number)[digits-1-i])
	return reverse_number

lychrell_count = 0
start_number = 1

while start_number<10000:
	number = start_number
	iteration = 1
	while iteration<50:
		if(is_palindrome(number + reverse(number))):
			break
		else:
			number += reverse(number)
			iteration += 1
			if(iteration==50):
				lychrell_count+=1
	start_number+=1
	
print("Answer: ",lychrell_count)

end = time.time()
print(end - start)