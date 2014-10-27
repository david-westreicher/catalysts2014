import socket
import time as t

KMH_TO_MS = 1000.0/3600.0

def readData():
	speed = sf.readline().strip().split()
	speed = float(speed[1])
	distance = sf.readline().strip().split()
	distance = float(distance[1])
	time = sf.readline().strip().split()
	time = float(time[1])
	speedlimit = sf.readline().strip().split()
	speedlimit = [float(x) for x in speedlimit[1:]]
	trafficLight = sf.readline().strip().split()
	if len(trafficLight)<=2:
		trafficLight = [0,0,0]
	else:
		trafficLight = [float(trafficLight[1]),trafficLight[2],float(trafficLight[3])]
	nextCar = sf.readline().strip().split()
	nextCar = [float(x) for x in nextCar[1:]]
	return speed, distance, time,speedlimit,trafficLight,nextCar

def move(speed, distance, timetr,speedlimit,trL,nextCar):
	msSpeed = speed*KMH_TO_MS
	desiredSpeed = speedlimit[0]

	# h4x no.1 ignore other cars by waiting :D
	if timetr<50:
		return 0,0
	
	# react to traffic light
	if trL[0]>0 and trL[2]>0:
		willPass = msSpeed*trL[2]>trL[0]
		if trL[1]=='Green':
		#GREEN
			if not willPass:
				# h4x no.2 approximate integration of speed, fugly
				if (desiredSpeed+msSpeed)*trL[2]/2 <= trL[0]+90:
					desiredSpeed = min(desiredSpeed,(trL[0]/(trL[2]+10))/KMH_TO_MS)
				if speed>desiredSpeed:
					return 0,100
		else:
		#RED
			if willPass:
				return 0,100
			else:
				desiredSpeed = min(desiredSpeed,(trL[0]/trL[2])/KMH_TO_MS)

	# brake, because of next speed limit
	if speedlimit[0]>speedlimit[2] and speedlimit[2]>0:
		deaccelTime = (speed-speedlimit[2])/21.84
		if msSpeed*deaccelTime >= speedlimit[1]:
			if speed>speedlimit[2]:
				return 0,100
			else:
				return 0,0

	# acelerate to desired speed
	acel =(desiredSpeed-speed)/2
	return max(0,min(100,acel)),0

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 7000))
sf = s.makefile()
while(True):
	speed, distance, time, speedlimit,trL,nextCar = readData()
	sf.readline()
	throttle,brake = move(speed, distance, time,speedlimit,trL,nextCar)
	sf.write('throttle '+str(throttle)+'\n')
	sf.write('brake '+str(brake)+'\n')
	sf.flush()
