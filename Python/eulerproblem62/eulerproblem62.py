import time
start = time.time()

def sort_digits(number):
	number_list = [int(x) for x in str(number)]
	digits = len(number_list)
	for i in range(0,digits-1):
		for j in range(0,digits-1):
			if(number_list[j]>number_list[j+1]):
				number_list[j+1], number_list[j] = number_list[j], number_list[j+1]
	return number_list
	
def number_equal(new):
	equal = 1
	for existing in cube_archive[:-1]:
		if new==existing:
			equal+=1
	return equal

cube_archive = []	
number=1
while(True):
	cube = number**3
	new = sort_digits(cube)
	cube_archive.append(new)
	if(number_equal(new)==5):
		break
	number+=1
	
for i in range(0, len(cube_archive)):
	if(cube_archive[i]==new):
		print("Answer: ",(i+1)**3)
		break

end = time.time()
print("Time: ",end-start)