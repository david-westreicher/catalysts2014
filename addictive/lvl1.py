import numpy as np
import itertools

f = open('lvl1/level1-3.in')
lines = f.read().splitlines()
for line in lines:
	print(line)
	nums = line.split(" ")
	rows = int(nums[0])
	cols = int(nums[1])
	print(str(rows)+"x"+str(cols))
	positions = [int(pos) for pos in nums[3:]]
	print(positions)
	result = []
	for pos in positions:
		result.append((pos-1)/cols+1)
		result.append((pos-1)%cols+1)
	for num in result:
		print(num),
	#print(result)
f.close()
