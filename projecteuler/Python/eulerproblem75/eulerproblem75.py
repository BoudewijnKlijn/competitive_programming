# https://en.wikipedia.org/wiki/Pythagorean_triple --> use euclid's formula, create primitive triples
# https://en.wikipedia.org/wiki/Coprime_integers

import time
start = time.time()

def is_coprime(num1,num2):
	divisor = 2
	while(divisor<=num1):
		if(num1%divisor==0 and num2%divisor==0):
			return False
		divisor+=1
	return True

L_list =[]
limit=1500000
upper = int((limit/2**0.5))
for m in range(2,upper+1):
	m2 = m*m
	for n in range(1,m):
		L = 2*m2+2*m*n
		if(L>limit):
			break
		if((n%2==0 or m%2==0) and is_coprime(n,m)):
			L_list.append(L)

count_L = []
for index in range(0,limit+2):
	count_L.append(0)

for trial in L_list:
	count_L[trial]+=1

for trial in L_list:
	mult=2
	while(mult*trial<limit):
		count_L[mult*trial]+=1
		mult+=1

answer=0
for count in count_L:
	if(count==1):
		answer+=1
print("Answer: ",answer)
end = time.time()
print("Time: ",end-start)