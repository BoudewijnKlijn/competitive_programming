import time
start = time.time()

number=[0]
max_index = 200
for i in range (1,max_index+1):
	number.append(0)

answer = 0
for a in range(1,100):
	for i in range (0,max_index+1):
		number[i]=0
		if(len(str(a))>1):
			number[max_index]=int(str(a)[1])
			number[max_index-1]=int(str(a)[0])
		else:
			number[max_index]=int(str(a)[0])
			
	for b in range(1,100):
		remainder = 0
		for i in range (0,max_index+1):
			dummy = number[max_index-i]*a+remainder
			number[max_index-i] = dummy%10
			remainder = dummy//10
			
		if(sum(number)>answer):
			answer = sum(number)

print("Answer: ",answer)

end = time.time()
print(end-start)