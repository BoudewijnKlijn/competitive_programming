number, answer = 0,0
while number<1000:
	if (number%3==0) or (number%5==0):
		answer+=number
	number+=1
print ("Answer: ", answer)