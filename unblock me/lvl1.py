import numpy as np
import itertools


def parseLine(line):
	split = line.split(" ")
	for i in range(len(split)/5):
		bid = int(split[i*5+0])
		orientation = split[i*5+1]
		y = int(split[i*5+2])-1
		x = int(split[i*5+3])-1
		length = int(split[i*5+4])
		ids.append(bid)
		orientations.append(orientation)
		positions.append([x,y])
		lengths.append(length)
	print(ids)


f = open('input/input-level1.txt')
lines = f.read().splitlines()
for line in lines:
	ids = []
	orientations = []
	positions = []
	lengths = []
	field = [[0 for i in range(100)] for j in range(100)]
	parseLine(line)
	for i in range(len(ids)):
		pos = positions[i]
		for j in range(lengths[i]):
			field[pos[0]+(j if orientations[i]=='v' else 0)][pos[1]+(j if orientations[i]=='h' else 0)]+=1
	print(line)
	overlap = False
	for i in range(100):
		#print(field[i])
		for j in range(100):
			if(field[i][j]>1):
				overlap = True
	print(overlap)
f.close()
