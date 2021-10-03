import time
start = time.time()

num_min_1, num_min_2, denom_min_1, denom_min_2, answer = 1, 1, 1, 0, 0
for expansion in range(1,1001):
	num = 2*num_min_1 + num_min_2
	denom = 2*denom_min_1 + denom_min_2	
	if(len(str(num))>len(str(denom))): answer+=1	
	num_min_2, num_min_1, denom_min_2, denom_min_1 = num_min_1, num, denom_min_1, denom	
print("Answer",answer)

end = time.time()
print("Time: ",end-start)