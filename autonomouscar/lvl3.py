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
	return speed, distance, time,speedlimit

energyConsumption = 0
lastTime = 0
accel = 2
timestep = 0
def move(speed, distance, timetr,speedlimit):
	global energyConsumption
	global lastTime
	global accel
	global timestep
	throttle = 0
	brake = 0
	#if(speed)
	#if(speed>speedlimit[0] or (speed>speedlimit[2] and speedlimit[1]<45 and speedlimit[1]>0)):
	#	throttle = 0
	#	brake = 100
	#	accel = 1.2
	#elif timestep%2==0:
	#	accel*=1.2
	#	throttle = min(50,accel)
	#if(distance>1600):
	#	throttle = 0
	#	brake = 100
	#energyConsumption += (((throttle/100.0)*310+1)/3.6)*(timetr-lastTime)
	#lastTime = timetr
	timestep+=1
	#print(energyConsumption)
	if(speed<speedlimit[0]-3 and timestep%3<=1):
		accel*=1.1
		throttle = min(30,accel)
	if(speed>speedlimit[0] or (speed>speedlimit[2] and speedlimit[1]<45 and speedlimit[1]>0)):
		brake = 100
		throttle = 0
		accel = 2
	return throttle,brake

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 7000))
sf = s.makefile()
while(True):
	speed, distance, time,speedlimit = readData()
	print(speed, distance, time,speedlimit)
	#update
	sf.readline()
	throttle,brake = move(speed, distance, time,speedlimit)
	sf.write('throttle '+str(throttle)+'\n')
	sf.write('brake '+str(brake)+'\n')
	sf.flush()
