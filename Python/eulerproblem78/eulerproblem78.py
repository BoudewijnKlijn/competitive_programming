def calc_P(n):
	result = 0
	ul = int(n**0.5)+1
	for k in range(1,ul+1):
		if(k%2==0): 
			mult = -1
		else: 
			mult = 1
		index1 = n - int(k/2*(3*k-1))
		index2 = n - int(k/2*(3*k+1))
		if(index1>=0):
			result += mult*P[index1]
		if(index2>=0):
			result += mult*P[index2]
	return result
	
global P
limit=100000 + 1
P = [0]*limit
P[0] = 1

for n in range(1,limit):
	P[n] = calc_P(n)
	if(P[n]%1000000==0):
		break
print("n:",n,"P(n)",P[n])
