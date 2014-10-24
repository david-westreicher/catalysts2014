import numpy as np
import itertools
import copy
from sets import Set
import operator

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
	def __init__(self):
		#self.nodeHash = hash(str(self.positions))
		pass
	
	def getPoss(self):
		poss = []
		return poss
	
	def __hash__(self):
		return self.nodeHash
		
	def __repr__(self):
		string = "\n"
		return string
	
	def __eq__(self, other):
		return True

	def finished(self):
		pass

def parseTime(time):
	arr = time.split(":")
	hours = int(arr[0])
	mins = int(arr[1])
	secs = int(arr[2])
	return [hours,mins,secs]

def toSecs(time):
	return time[0]*3600+time[1]*60+time[2]
def compute(p):
	beginStr = p.next()
	begin = toSecs(parseTime(beginStr))
	startPoint = int(p.next())
	startPoints = [startPoint for i in range(10000)]
	subNum = int(p.next())
	submissions = []
	uidPoints = {}
	for i in range(subNum):
		uid = int(p.next())
		uidPoints[uid] = 0
		timeStr = p.next()
		time = toSecs(parseTime(timeStr))
		status = p.next()
		taskID = int(p.next())
		if status == "correct" and time>=begin:
			submissions.append([uid,time,timeStr,status,taskID])
			
	
	sortedSubs = []
	while len(submissions)>0:
		minIndex = -1
		minSubmissionTime = 1000000
		for i in range(len(submissions)):
			if submissions[i][1]<minSubmissionTime and submissions[i][1]>=begin:
				minSubmissionTime = submissions[i][1]
				minIndex = i
		sortedSubs.append(submissions[minIndex])
		del submissions[minIndex]
		
	#print(sortedSubs)
	
	for sub in sortedSubs:
		if startPoints[sub[4]]>0:
			uidPoints[sub[0]] += startPoints[sub[4]]
			startPoints[sub[4]]-=1
	
	#print(uidPoints)
	sortedByScore = sorted(uidPoints.items(), key=operator.itemgetter(1))[::-1]
	sortedTrough = {}
	for r in sortedByScore:
		nlist = None
		if r[1] in sortedTrough.keys():
			nlist = sortedTrough[r[1]]
		else:
			nlist = []
			sortedTrough[r[1]] = nlist
		nlist.append(r[0])
	
	for key in sortedTrough:
		tmpArr = sortedTrough[key]
		sortedTrough[key] = sorted(tmpArr, reverse=False)
	for entry in  sorted(sortedTrough.items(), key=operator.itemgetter(0))[::-1]:
		points = entry[0]
		for uid in entry[1]:
			print(str(points)+" "+str(uid)),
	print("\n\n\n")

p = Parser('input/input-level5.txt')
while p.has():
	compute(p)
p.close()
