import numpy as np
import itertools
import AStar

direction = {'N':[-1,0],'E':[0,1],'S':[1,0],'W':[0,-1]}
def indexToPos(index,cols):
	row = (index-1)/cols+1
	column = (index-1)%cols+1
	return (row,column)

def parsePath(nums,startIndex,cols):
	#print(nums[startIndex:(startIndex+10)])
	color = int(nums[startIndex])
	startPos = nums[startIndex+1]
	length = int(nums[startIndex+2])
	path = nums[(startIndex+3):(startIndex+3+length)]
	startPos = indexToPos(int(startPos),cols)
	return (color,startPos,path), startIndex+3+length

def drawGF(gamefield):
	for i in range(gamefield.shape[0]):
		for j in range(gamefield.shape[1]):
			if(gamefield[i][j]==0):
				print(' '),
			elif(gamefield[i][j]==-1):
				print('x'),
			else:
				print(gamefield[i][j]),
		print("\n"),

def plot(H):
	fig = plt.figure(figsize=(6, 3.2))
	ax = fig.add_subplot(111)
	ax.set_title('colorMap')
	plt.imshow(H, cmap='Greys',  interpolation='nearest')
	ax.set_aspect('equal')

	cax = fig.add_axes([0.12, 0.1, 0.78, 0.8])
	cax.get_xaxis().set_visible(False)
	cax.get_yaxis().set_visible(False)
	cax.patch.set_alpha(0)
	cax.set_frame_on(False)
	plt.colorbar(orientation='vertical')
	plt.show()
		
def isPathValid(gamefield,colorToRealPos,path):
	#start point always correct
	startPos = np.asarray(path[1])
	visitedPos =[startPos]
	#print(startPos)
	currentStep = 0
	fail = False
	for step in path[2]:
		startPos = startPos.copy() + direction[step]
		#print(startPos)
		currentStep+=1
		#goes out of bounds
		if(startPos[0]>rows or startPos[0]<1 or startPos[1]<1 or startPos[1]>cols):
			fail = True
			#print("Outofbounds")
			break
		#crosses other line
		gfval = gamefield[startPos[0]-1][startPos[1]-1]
		if(gfval!=0 and gfval!=path[0]):
			fail = True
			#print("crossed other line")
			break
			
		
		#crosses itself
		for visited in visitedPos:
			if(visited[0]==startPos[0] and visited[1]==startPos[1]):
				fail = True
				#print("already visited")
				break
		#touches point of different color
		#for color,poss in enumerate(colorToRealPos):
		#	if((color+1)!=path[0]):
		#		poss = colorToRealPos[color]
		#		visited = poss[0]
		#		if(visited[0]==startPos[0] and visited[1]==startPos[1]):
		#			fail = True
		#			print("color here")
		#			break
		#		visited = poss[1]
		#		if(visited[0]==startPos[0] and visited[1]==startPos[1]):
		#			fail = True
		#			print("color here")
		#			break
		if(fail):
			break
		visitedPos.append(startPos)
		
	#valid endpoint
	if(not fail):
		poss = colorToRealPos[path[0]-1]
		if(not((poss[0][0]==startPos[0] and poss[0][1]==startPos[1]) or (poss[1][0]==startPos[0] and poss[1][1]==startPos[1]))):
			fail = True
			
	#if(fail):
	#	print(-1),
	#	print(currentStep)
	#else:
	#	print(1),
	#	print(currentStep)
	return visitedPos, not fail
def pathOnGF(gamefield,path):
	startPos = np.asarray(path[1])
	for step in path[2]:
		startPos = startPos.copy() + direction[step]
		gamefield[startPos[0]-1][startPos[1]-1] = path[0]
		
def connectable(gamefield,pos1,pos2):
	print(pos1)
	
	return False

def parseTest(startIndex,result):
	rows = int(nums[startIndex])
	cols = int(nums[startIndex+1])
	gamefield = np.zeros((rows,cols),dtype=np.int)
	positionscolorsnum =  int(nums[startIndex+2])*2+3+startIndex
	print(str(rows)+"x"+str(cols))
	positionscolors = [int(pos) for pos in nums[(startIndex+3):positionscolorsnum]]
	numberOfPaths = int(nums[positionscolorsnum])
	newIndex = positionscolorsnum+1
	paths = []
	print("parsing paths")
	for i in range(numberOfPaths):
		path, newIndex = parsePath(nums,newIndex,cols)
		paths.append(path)
		#print(path)
	print("paths parsed")
	#print(positionscolors)
	positions = []
	colors = []
	for i, poscol in enumerate(positionscolors):
		if(i%2==0):
			positions.append(poscol)
		else:
			colors.append(poscol)
	print("colorspos parsed")
	#colorToPos = {}
	colorToPos = [[] for i in range(len(colors)/2)]
	print(len(colorToPos))
	for i, color in enumerate(colors):
		#if(not(color in colorToPos.keys())):
		#	colorToPos[color] = []
		#arr = colorToPos[color]
		colorToPos[color-1].append(positions[i])
		#print(colorToPos[color-1])
	print("colorToPos parsed")
	#print(colorToPos)
	colorToRealPos =  [[] for i in range(len(colors)/2)]
	for color in range(0,len(colorToPos)):
		pos = colorToPos[color]
		pos1 = indexToPos(pos[0],cols)
		pos2 = indexToPos(pos[1],cols)
		colorToRealPos[color] = [pos1,pos2]
		gamefield[pos1[0]-1,pos1[1]-1] = color+1
		gamefield[pos2[0]-1,pos2[1]-1] = color+1
	stati = [0 for i in range(len(colorToRealPos))]
	for i, path in enumerate(paths):
		stati[path[0]-1] = 1
		pathOnGF(gamefield,path)
	
	drawGF(gamefield)
	
	
	for i,poss in enumerate(colorToRealPos):
		if(stati[i]==0):
			pos1 = np.asarray(poss[0])-1
			pos2 = np.asarray(poss[1])-1
			tmpgamefield = gamefield.copy()
			tmpgamefield[tmpgamefield==i+1] = 0
			tmpgamefield[tmpgamefield>0] = -1
			#drawGF(tmpgamefield)
			astar = AStar.AStar(AStar.SQ_MapHandler(tmpgamefield.flatten(),gamefield.shape[1],gamefield.shape[0]))
			start = AStar.SQ_Location(pos1[1],pos1[0])
			end = AStar.SQ_Location(pos2[1],pos2[0])
			#print("From "+str(pos1)+" to: "+str(pos2))
			p = astar.findPath(start,end)
			#if(p is not None):
			#	for p in p.nodes:
			#		print(str(p.location.x)+" "+str(p.location.y))
			stati[i] = 2 if p is not None else 3
		
	result.extend(stati)
	return result,newIndex
		
	
f = open('lvl5/level5-4.in')
lines = f.read().splitlines()
for line in lines:
	#line = "1 5 5 8 1 1 3 2 4 3 7 4 9 4 20 3 18 2 25 1 1 2 3 5 S S "
	line = line.strip()
	line = ' '.join(line.split())
	print(line)
	nums = line.split(" ")
	numberOfTests = int(nums[0])
	print("Number of tests: "+str(numberOfTests))
	result = []
	index = 1
	for i in range(numberOfTests):
		result,index = parseTest(index,result)
	print("Result")
	for r in result:
		print(r),
			
f.close()
