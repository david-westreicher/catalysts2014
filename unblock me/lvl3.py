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
	moves = split[3+blockNum*5:]
	
	print(line)
	#print(ids)
	#print(blocks)
	#print(realMoves)
			
	#check if outside
	
	for i in range(len(ids)):
		pos = positions[i]
		for j in range(lengths[i]):
			field[pos[0]+(j if orientations[i]=='h' else 0)][pos[1]+(j if orientations[i]=='v' else 0)]+=1
	
	#printField(field)
	
	statics = []
	for i in range(len(ids)):
		#print("id "+str(ids[i]))
		pos = positions[i]
		hit = False
		if orientations[i]=='v':
			hit |= isOccu(field,pos[0],pos[1]-1)
			hit |= isOccu(field,pos[0],pos[1]+lengths[i])
		if orientations[i]=='h':
			hit |= isOccu(field,pos[0]-1,pos[1])
			hit |= isOccu(field,pos[0]+lengths[i],pos[1])
		#print(hit,pos,lengths[i])
		if not hit:
			statics.append(i)
	for st in statics:
		print(st),
	print("\n"),
	
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

f = open('input/input-level3.txt')
lines = f.read().splitlines()
for line in lines:
	ids = []
	orientations = []
	positions = []
	lengths = []
	moves = []
	parseLine(line)

f.close()
