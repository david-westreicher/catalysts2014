import numpy as np
import itertools


def parseLine(line):
	split = line.split(" ")
	width = int(split[0])
	height = int(split[1])
	blockNum = int(split[2])
	field = [[0 for i in range(width)] for j in range(height)]
	blocks = split[3:3+blockNum*5]
	for i in range(blockNum):
		bid = int(blocks[i*5+0])
		orientation = blocks[i*5+1]
		y = int(blocks[i*5+2])-1
		x = int(blocks[i*5+3])-1
		length = int(blocks[i*5+4])
		ids.append(bid)
		orientations.append(orientation)
		positions.append([x,y])
		lengths.append(length)
	moves = split[3+blockNum*5:]
	realMoves = []
	for i in range(len(moves)/2):
		realMoves.append([int(moves[i*2+0]),int(moves[i*2+1])])
	print(line)
	#print(ids)
	#print(blocks)
	#print(realMoves)
	for move in realMoves:
		pos = positions[move[0]]
		if(orientations[move[0]]=='h'):
			pos[1]+=move[1]
		if(orientations[move[0]]=='v'):
			pos[0]+=move[1]
		for j in range(lengths[move[0]]):
			currY = pos[0]+(j if orientations[i]=='v' else 0)
			currX = pos[1]+(j if orientations[i]=='h' else 0)
			if( currX<0 or currY<0 or currX>=width or currY>=height):
				print("outside")
				print("true")
				return
			
	#check if outside
	
	for i in range(len(ids)):
		pos = positions[i]
		for j in range(lengths[i]):
			field[pos[0]+(j if orientations[i]=='v' else 0)][pos[1]+(j if orientations[i]=='h' else 0)]+=1
	printField(field)
	
	overlap = False
	for i in range(height):
		for j in range(width):
			if(field[i][j]>1):
				overlap = True
	print(overlap)
	
def printField(field):
	for arr in field:
		print(arr)
	print("###\n")

f = open('input/input-level2.txt')
lines = f.read().splitlines()
for line in lines:
	ids = []
	orientations = []
	positions = []
	lengths = []
	moves = []
	parseLine(line)

f.close()
