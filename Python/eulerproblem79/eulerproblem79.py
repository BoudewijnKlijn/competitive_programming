# import textfile -> create list with only numbers
filename = 'p079_keylog.txt' 
fin=open(filename,'r')
mylist = []
for i in range(0,50):
	mylist.append(fin.readline())
	mylist[i] = mylist[i][:3]

before_x_comes = [[-1]]*10
after_x_comes = [[-1]]*10
for i in range(1,10):
	before_x_comes[i] = [int(str(i)*3)]
	after_x_comes[i] = [int(str(i)*3)]

for i in range(0,50):
	for pos1 in range(0,3):
		value1 = int(mylist[i][pos1])
		for pos2 in range(0,3):
			value2 = int(mylist[i][pos2])
			if(pos1>pos2):
				if not(value2 in before_x_comes[value1]):
					before_x_comes[value1] = before_x_comes[value1] + [value2]
			if(pos1<pos2):
				if not(value2 in after_x_comes[value1]):
					after_x_comes[value1] = after_x_comes[value1] + [value2]
					
for i in range(0,10):
	before_x_comes[i].sort()
	after_x_comes[i].sort()
print("BEFORE",before_x_comes)
print("AFTER",after_x_comes)
					