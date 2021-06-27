def count_digits(number):
	return len(str(number))
	
number = 1
answer = 0
while(number<10):
	for power in range(1,22):
		if(power==count_digits(number**power)):
			# print("Number: ", number,", Power: ",power,", Digits: ",count_digits(number**power))
			answer+=1
	number+=1
	
print("Answer: ", answer)