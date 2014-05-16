import numpy as np
import itertools


def indexToPos(index,cols):
	row = (index-1)/cols+1
	column = (index-1)%cols+1
	return (row,column)
	
f = open('lvl2/level2-3.in')
lines = f.read().splitlines()
for line in lines:
	print(line)
	nums = line.split(" ")
	rows = int(nums[0])
	cols = int(nums[1])
	print(str(rows)+"x"+str(cols))
	positionscolors = [int(pos) for pos in nums[3:]]
	positions = []
	colors = []
	for i, poscol in enumerate(positionscolors):
		if(i%2==0):
			positions.append(poscol)
		else:
			colors.append(poscol)
	print(positionscolors)
	print(positions)
	print(colors)
	colorToPos = {}
	for i, color in enumerate(colors):
		if(not(color in colorToPos.keys())):
			colorToPos[color] = []
		arr = colorToPos[color]
		arr.append(positions[i])
	#for (pos,col) in zip(positions,colors):
	result = []
	for colorpos in colorToPos:
		pos = colorToPos[colorpos]
		pos1 = indexToPos(pos[0],cols)
		pos2 = indexToPos(pos[1],cols)
		dist = abs(pos1[0]-pos2[0])+abs(pos1[1]-pos2[1])
		result.append(dist)
		print(colorpos),
		print(pos1),
		print(pos2)
	for r in result:
		print(r),
	#print(result)
f.close()
