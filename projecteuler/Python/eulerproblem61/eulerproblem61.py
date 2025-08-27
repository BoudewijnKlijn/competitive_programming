import sys
import time
start = time.time()

global poly
poly = [[1035],[1024],[1001],[1035],[1071],[1045]]
for n in range(46,141):
	p3 = int(n*(n+1)/2)
	poly[0].append(p3)
	
for n in range(33,100):
	p4 = n*n
	poly[1].append(p4)
	
for n in range(28,82):
	p5 = int(n*(3*n-1)/2)
	poly[2].append(p5)
	
for n in range(24,71):
	p6 = n*(2*n-1)
	poly[3].append(p6)
	
for n in range(22,64):
	p7 = int(n*(5*n-3)/2)
	poly[4].append(p7)
	
for n in range(20,59):
	p8 = n*(3*n-2)
	poly[5].append(p8)

def ending(num):
	return str(num)[-2:]
	
def starting(num):
	return str(num)[:2]
	
def verify_end_start(index_1,index_2):
	return ending(chain[index_1])==starting(chain[index_2])
	
def unique_poly_set(position, value):
	return value not in chain_poly_set[:position]

def search(needle, exclude_set, bool_start):
	for haystack_set in range(0,6):
		if haystack_set not in exclude_set:
			for trial_num in poly[haystack_set]:
				if(bool_start==1):
					if(starting(needle)==ending(trial_num)):
						return 1
				else:
					if(ending(needle)==starting(trial_num)):
						return 1
	return 0	

updated=1
while(updated==1):
	updated=0
	for poly_set in range(0,6):
		for num_1 in poly[poly_set]:
			if(search(num_1,[poly_set],0)==0):
				poly[poly_set].remove(num_1)
				updated=1
				
	for poly_set in range(0,6):
		for num_1 in poly[poly_set]:
			if(search(num_1,[poly_set],1)==0):
				poly[poly_set].remove(num_1)
				updated=1
				
chain=[0,0,0,0,0,0]
chain_poly_set=[-1,-1,-1,-1,-1,-1]
for poly_set_1 in range(0,6):
	chain_poly_set[0] = poly_set_1
	for num_1 in poly[poly_set_1]:
		chain[0] = num_1
		for poly_set_2 in range(0,6):
			if(unique_poly_set(1, poly_set_2)):
				chain_poly_set[1] = poly_set_2
				for num_2 in poly[poly_set_2]:
					chain[1] = num_2
					if(verify_end_start(0,1)):
						for poly_set_3 in range(0,6):
							if(unique_poly_set(2, poly_set_3)):
								chain_poly_set[2] = poly_set_3
								for num_3 in poly[poly_set_3]:
									chain[2] = num_3
									if(verify_end_start(1,2)):
										for poly_set_4 in range(0,6):
											if(unique_poly_set(3, poly_set_4)):
												chain_poly_set[3] = poly_set_4
												for num_4 in poly[poly_set_4]:
													chain[3] = num_4
													if(verify_end_start(2,3)):
														for poly_set_5 in range(0,6):
															if(unique_poly_set(4, poly_set_5)):
																chain_poly_set[4] = poly_set_5
																for num_5 in poly[poly_set_5]:
																	chain[4] = num_5
																	if(verify_end_start(3,4)):
																		for poly_set_6 in range(0,6):
																			if(unique_poly_set(5, poly_set_6)):
																				chain_poly_set[5] = poly_set_6
																				for num_6 in poly[poly_set_6]:
																					chain[5] = num_6
																					if(verify_end_start(4,5) and verify_end_start(5,0)):
																						print("Answer: ",sum(chain))
																						end = time.time()
																						print("Time: ",end-start)
																						sys.exit()
