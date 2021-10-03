def b2a(bits):
	number = 0
	digits = len(bits)
	for i in range(0,digits):
		if(bits[i]==1):
			number += 2**(digits-1-i)
	return number

def a2b(number):
	power=6
	bit = [0,0,0,0,0,0,0]
	while(number>0):
		if(number>=2**power):
			number -= 2**power
			bit[6-power] = 1
		else:
			power-=1
	return bit

def xor(bit_1,bit_2):
	bit = [0,0,0,0,0,0,0]
	for i in range(0,len(bit_1)):
		if( (bit_1[i] or bit_2[i]) and not (bit_1[i] and bit_2[i]) ):
			bit[i]=1
	return bit
	
# import textfile -> create list with only numbers
filename = 'p059_cipher.txt' 
fin=open(filename,'r')
mylist = fin.readline()
index_number = 0
cipher_list = [int(mylist[index_number])]
for index in range(1,len(mylist)):
	if(mylist[index]==','):
		index_number+=1
		cipher_list.append(0)
	else:
		cipher_list[index_number] = cipher_list[index_number]*10 + int(mylist[index])

# solve the problem by trying every possible key (3 lowercase letters), search in deciphered text for likely word
alphabet = 'abcdefghijklmnopqrstuvwxyz'
search = 'euler'
answer = 0
for key1 in range(6,7):
	print(key1)
	for key2 in range(14,15):
		for key3 in range(3,4):
			decipher_text = ''
			use_key = 1
			for index in range(0,len(cipher_list)):
				if(use_key==1):
					num_key = ord(alphabet[key1])
					use_key=2
				elif(use_key==2):
					num_key = ord(alphabet[key2])
					use_key=3
				elif(use_key==3):
					num_key = ord(alphabet[key3])
					use_key=1		
				decipher = b2a(xor(a2b(cipher_list[index]),a2b(num_key)))
				decipher_text += chr(decipher)
				answer += decipher
			if (search in decipher_text):
				print("Key1: ",key1,", Key2: ",key2,", Key3: ",key3)
			
print(decipher_text)
print("Answer: ",answer)			
# print(xor(a2b(32),a2b(111)))
# print(b2a(xor(a2b(32),a2b(111))))
# print(b2a(xor(a2b(32),a2b(b2a(xor(a2b(111),a2b(32)))))))