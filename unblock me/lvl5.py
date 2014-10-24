import numpy as np
import itertools
import copy
from sets import Set

class Found(Exception):pass

class Parser:
	def __init__(self, pFile):
		self.pFile = pFile
		self.f = None
		self.lineIndex = 0
		self.index = 0
		self.lines = []
		self.line = []
	
	def next(self):
		if self.f is None:
			self.f = open(self.pFile)
			lines = self.f.read().splitlines()
			for line in lines:
				if len(line)>0:
					self.lines.append(line)
			self.line = self.lines[0].split()
			#print(self.lines[0])
		if self.index>=len(self.line):
			self.lineIndex+=1
			if self.lineIndex>=len(self.lines):
				print("\n######## END OF FILE!!!!#######\n")
				self.f.close()
				return
			self.line = self.lines[self.lineIndex].split()
			#print(self.lines[self.lineIndex])
			self.index = 0
		self.index +=1
		return self.line[self.index-1]
		
	def parsed(self):
		return " ".join(self.line[0:self.index])
	
	def close(self):
		if not self.f is None:
			self.f.close()
			
	def has(self):
		if self.f is None:
			return True
		if self.lineIndex>=len(self.lines)-1 and self.index==len(self.line):
			return False
		else:
			return True

class Node:
	def __init__(self, field, positions,oldMoves=[]):
		self.field = field
		self.positions = positions
		self.moves = []
		self.nodeHash = hash(str(self.positions))
		for move in oldMoves:
			self.moves.append(move)
	
	def getPoss(self):
		poss = []
		for i in range(len(self.positions)):
			pos = self.positions[i]
			length = lengths[i]
			if orientations[i]=='h':
				self.possMove(poss,length,pos,1,0,i)
				self.possMove(poss,length,pos,-1,0,i)
			if orientations[i]=='v':
				self.possMove(poss,length,pos,0,1,i)
				self.possMove(poss,length,pos,0,-1,i)
		return poss
	
	def __hash__(self):
		return self.nodeHash
		
	def __repr__(self):
		string = "\n"
		for x in range(len(self.field[0])):
			for y in range(len(self.field)):
				string+=str(self.field[y][x])+" "
			string+="\n"
		string+="###\n"
		return string
	
	def __eq__(self, other):
		for i in range(len(self.positions)):
			if self.positions[i][0]!=other.positions[i][0] or self.positions[i][1]!=other.positions[i][1]:
				return False
		return True
		
	def possMove(self,poss,length,pos,xD,yD,index):
		x = pos[0]
		if xD>0:
			x+=length
		elif xD<0:
			x-=1
		y = pos[1]
		if yD>0:
			y+=length
		elif yD<0:
			y-=1
		#print(pos,xD,yD,length,index)
		#print("checking ",x,y)
		if isOccu(self.field,x,y):
			tmpField = [[0 for i in range(len(self.field[0]))] for j in range(len(self.field))]
			tmpPos = [tmpp[:] for tmpp in self.positions]
			tmpPos[index][0]+=xD
			tmpPos[index][1]+=yD
			populate(tmpField,tmpPos)
			n = Node(tmpField,tmpPos,self.moves)
			n.moves.append([index,xD+yD])
			poss.append(n)

	def finished(self):
		hit = False
		#printField(self.field)
		for i in range(self.positions[0][0]+lengths[0],len(self.field)):
			if self.field[i][self.positions[0][1]]>0:
				hit = True
		return not hit
		
	def equals(self,otherNode):
		for i in range(len(self.positions)):
			if self.positions[i][0]!=otherNode.positions[i][0] or self.positions[i][1]!=otherNode.positions[i][1]:
				return False
		return True

def compute(p):
	global lengths
	global orientations
	orientations = []
	positions = []
	lengths = []
	width = int(p.next())
	height = int(p.next())
	blockNum = int(p.next())
	field = [[0 for i in range(height)] for j in range(width)]
	for i in range(blockNum):
		bid = int(p.next())
		orientation = p.next()
		x = int(p.next())-1
		y = int(p.next())-1
		length = int(p.next())
		orientations.append(orientation)
		positions.append([x,y])
		lengths.append(length)
	
	print(p.parsed())
	
	#print(blocks)
	populate(field,positions)
	#printField(field)
	n = Node(field,positions)
	allNodes = Set([n])
	currentLayer =[n]
	try:
		for i in range(100):
			#print("layer"+str(i))
			newLayer = []
			for node in currentLayer:
				if node.finished():
					print("FINISHED")
					#print(node)
					for move in node.moves:
						print(str(move[0])+" "+str(move[1])), 
					print("\n")
					raise Found
				#print(node)
				#print(hash(node))
				for child in node.getPoss():
					if not child in allNodes:
						newLayer.append(child)
						allNodes.add(child)
			currentLayer = newLayer
	except Found:
		pass
		

def populate(field,poss):
	for i in range(len(poss)):
		pos = poss[i]
		for j in range(lengths[i]):
			x = pos[0]+(j if orientations[i]=='h' else 0)
			y = pos[1]+(j if orientations[i]=='v' else 0)
			#if(x<0 or x>=len(field) or y<0 or y>=len(field[0])):
				#print("end in "+str(currentMove))
			#	return
			field[x][y]=i+1
	
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
	
p = Parser('input/input-level5.txt')
while p.has():
	compute(p)
p.close()

