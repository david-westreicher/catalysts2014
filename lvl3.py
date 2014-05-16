import numpy as np
import itertools

direction = {'N':[-1,0],'E':[0,1],'S':[1,0],'W':[0,-1]}
def indexToPos(index,cols):
	row = (index-1)/cols+1
	column = (index-1)%cols+1
	return (row,column)

def parsePath(nums,startIndex):
	color = int(nums[startIndex])
	startPos = nums[startIndex+1]
	length = int(nums[startIndex+2])
	path = nums[(startIndex+3):(startIndex+3+length)]
	startPos = indexToPos(int(startPos),cols)
	return (color,startPos,path)
	
f = open('lvl3/level3-7.in')
lines = f.read().splitlines()
for line in lines:
	#line = "5 5 8 7 1 9 1 10 2 16 3 17 2 19 4 20 3 25 4 1 1 9 3 S S W"
	print(line)
	nums = line.split(" ")
	rows = int(nums[0])
	cols = int(nums[1])
	positionscolorsnum =  int(nums[2])*2+3
	print(str(rows)+"x"+str(cols))
	positionscolors = [int(pos) for pos in nums[3:positionscolorsnum]]
	numberOfPaths = nums[positionscolorsnum]
	path = parsePath(nums,positionscolorsnum+1)
	print(positionscolors)
	positions = []
	colors = []
	for i, poscol in enumerate(positionscolors):
		if(i%2==0):
			positions.append(poscol)
		else:
			colors.append(poscol)
	colorToPos = {}
	for i, color in enumerate(colors):
		if(not(color in colorToPos.keys())):
			colorToPos[color] = []
		arr = colorToPos[color]
		arr.append(positions[i])
	colorToRealPos = {}
	for colorpos in colorToPos:
		pos = colorToPos[colorpos]
		pos1 = indexToPos(pos[0],cols)
		pos2 = indexToPos(pos[1],cols)
		colorToRealPos[colorpos] = [pos1,pos2]
	print(colorToRealPos)
	print(path)
	#start point always correct
	startPos = np.asarray(path[1])
	visitedPos =[startPos]
	print(startPos)
	currentStep = 0
	fail = False
	for step in path[2]:
		startPos = startPos.copy() + direction[step]
		print(startPos)
		currentStep+=1
		#goes out of bounds
		if(startPos[0]>rows or startPos[0]<1 or startPos[1]<1 or startPos[1]>cols):
			fail = True
			print("Outofbounds")
			break
		#crosses itself
		for visited in visitedPos:
			if(visited[0]==startPos[0] and visited[1]==startPos[1]):
				fail = True
				print("already visited")
				break
		#touches point of different color
		for color in colorToRealPos:
			if(color!=path[0]):
				poss = colorToRealPos[color]
				visited = poss[0]
				if(visited[0]==startPos[0] and visited[1]==startPos[1]):
					fail = True
					print("color here")
					break
				visited = poss[1]
				if(visited[0]==startPos[0] and visited[1]==startPos[1]):
					fail = True
					print("color here")
					break
		if(fail):
			break
		visitedPos.append(startPos)
		
	#valid endpoint
	if(not fail):
		poss = colorToRealPos[path[0]]
		if(not((poss[0][0]==startPos[0] and poss[0][1]==startPos[1]) or (poss[1][0]==startPos[0] and poss[1][1]==startPos[1]))):
			fail = True
			
	if(fail):
		print(-1),
		print(currentStep)
	else:
		print(1),
		print(currentStep)
		
	#for (pos,col) in zip(positions,colors):
	result = []
	for r in result:
		print(r),
	#print(result)
f.close()
