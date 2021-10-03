filename = 'p079_keylog.txt' 
fin=open(filename,'r')
mylist = []
for i in range(0,50):
	mylist.append(fin.readline())
	mylist[i] = mylist[i][:3]
print(mylist)