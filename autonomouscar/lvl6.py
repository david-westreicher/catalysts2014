import socket
import time as t
import math

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
	if(len(trafficLight)>3):
		trafficLight = [float(trafficLight[1]),trafficLight[2],float(trafficLight[3])]
	else:
		trafficLight = [0,'Green',0]
	nextCar = sf.readline().strip().split()
	nextCar = [float(x) for x in nextCar[1:]]
	return speed, distance, time,speedlimit,trafficLight,nextCar

energyConsumption = 0
lastTime = 0
accel = 2
timestep = 0
def move(speed, distance, timetr,speedlimit,trafficLight,nextCar):
	global energyConsumption
	global lastTime
	global accel
	global timestep
	throttle = 0
	brake = 0
	if(nextCar[0]>0):
		if (speed>nextCar[1] and nextCar[0]<15):
			throttle = 0
			brake = 100 if nextCar[0]<10 else 50
			accel = 2
		else:
			throttle = accel
			accel*=1.2
	else:
		throttle = accel
		accel*=1.2
	if speed>speedlimit[0] or (speed>speedlimit[2] and speedlimit[1]<60 and speedlimit[1]>0):
		brake = 100
		throttle = 0
		accel = 2
	return throttle,brake

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 7000))
sf = s.makefile()
while(True):
	speed, distance, time,speedlimit,trafficLight,nextCar = readData()
	print(speed, distance, time,speedlimit,trafficLight,nextCar)
	#update
	sf.readline()
	throttle,brake = move(speed, distance, time,speedlimit,trafficLight,nextCar)
	sf.write('throttle '+str(throttle)+'\n')
	sf.write('brake '+str(brake)+'\n')
	sf.flush()
