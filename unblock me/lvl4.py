import numpy as np
import itertools


def parseLine(line):
	split = line.split(" ")
	width = int(split[0])
	height = int(split[1])
	blockNum = int(split[2])
	field = [[0 for i in range(height)] for j in range(width)]
	blocks = split[3:3+blockNum*5]
	for i in range(blockNum):
		bid = int(blocks[i*5+0])
		orientation = blocks[i*5+1]
		x = int(blocks[i*5+2])-1
		y = int(blocks[i*5+3])-1
		length = int(blocks[i*5+4])
		ids.append(bid)
		orientations.append(orientation)
		positions.append([x,y])
		lengths.append(length)
	moves = split[4+blockNum*5:]
	realMoves = []
	for i in range(len(moves)/2):
		realMoves.append([int(moves[i*2+0]),int(moves[i*2+1])])
	print(realMoves)
	
	print(line)
	#print(ids)
	#print(blocks)
	#print(realMoves)
			
	#check if outside
	
	for currentMove in range(len(realMoves)):
		initField(field)
		m = realMoves[currentMove]
		if(orientations[m[0]]=='h'):
			positions[m[0]][0]+=m[1]
		else:
			positions[m[0]][1]+=m[1]
		#print(m)
		for i in range(len(ids)):
			pos = positions[i]
			for j in range(lengths[i]):
				x = pos[0]+(j if orientations[i]=='h' else 0)
				y = pos[1]+(j if orientations[i]=='v' else 0)
				if(x<0 or x>=width or y<0 or y>=height):
					print("end in "+str(currentMove))
					return
				field[x][y]+=1
		#printField(field)
		if(checkField(field)):
			print("end in "+str(currentMove))
			return
	print("end in "+str(len(realMoves)))
	
	
def checkField(field):
	overlap = False
	for i in range(len(field)):
		for j in range(len(field[0])):
			if(field[i][j]>1):
				overlap = True
	return overlap
	
def initField(field):
	for arr in field:
		for i in range(len(arr)):
			arr[i]=0
	
def isOccu(field, x,y):
	#print(x,y)
	if(x<0 or y<0 or x>=len(field) or y>=len(field[0])):
		#print("outside move")
		return False
	else:
		if(field[x][y]>0):
			#print("hit move")
			return False
	return True
	
def printField(field):
	for x in range(len(field[0])):
		for y in range(len(field)):
			print(field[y][x]),
		print("\n"),
	print("###\n")

f = open('input/input-level4.txt')
lines = f.read().splitlines()
for line in lines:
	ids = []
	orientations = []
	positions = []
	lengths = []
	moves = []
	parseLine(line)

f.close()
