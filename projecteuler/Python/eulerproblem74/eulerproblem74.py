

fac_list = [1]
for i in range(1,10):
	fac_list.append(fac_list[i-1]*i)

answer = 0
for num in range(0,1000000):
	chain = []
	sum = num
	while not num in chain:
		chain.append(num)
		sum = 0
		for digit in str(num):
			sum += fac_list[int(digit)]
		num = sum
	if(len(chain)==60):
		answer+=1
		print("Answer: ",answer)

print("Answer: ",answer)