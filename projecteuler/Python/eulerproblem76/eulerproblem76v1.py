import matplotlib.pyplot as plt

solution_list = [[[0]]]
solution_list.append([[1]])
x = [0,1]
y = [0,0]

for solution in range(2,26):
	x.append(solution)
	print(solution, end="")
	solution_list.append([[solution]])
	for first_digit in range(solution-1,0,-1):
		existing_solution = solution-first_digit
		for index_existing in range(0,len(solution_list[existing_solution])):
			new = [first_digit] + solution_list[existing_solution][index_existing]
			new.sort()
			if new not in solution_list[solution]:
				solution_list[solution].append(new)
	print(" ",len(solution_list[solution])-1)
	y.append(len(solution_list[solution])-1)
	
plt.plot(x,y)
plt.show()
plt.clf()