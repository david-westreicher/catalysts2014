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
	trafficLight = [float(trafficLight[1]),trafficLight[2],float(trafficLight[3])]
	return speed, distance, time,speedlimit,trafficLight

energyConsumption = 0
lastTime = 0
accel = 2
timestep = 0
def move(speed, distance, timetr,speedlimit,trafficLight):
	global energyConsumption
	global lastTime
	global accel
	global timestep
	throttle = 0
	brake = 0
	timestep+=1
	if(speed<speedlimit[0]-3 and timestep%2==0):
		throttle =40
	trL = False
	msSpeed = speed*KMH_TO_MS
	print(msSpeed,trafficLight[2],trafficLight[0])
	if (trafficLight[1]=='Red' or trafficLight[1]=='RedYellow' or trafficLight[1]=='Yellow') and msSpeed*trafficLight[2]>trafficLight[0]-5:
		trL = True
	if (trafficLight[1]=='Green' and msSpeed*trafficLight[2]<trafficLight[0]-5):
		trL = True
	if speed>speedlimit[0] or (speed>speedlimit[2] and speedlimit[1]<45 and speedlimit[1]>0) or trL:
		brake = 100
		throttle = 0
		accel = 2
	return throttle,brake

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 7000))
sf = s.makefile()
while(True):
	speed, distance, time,speedlimit,trafficLight = readData()
	print(speed, distance, time,speedlimit,trafficLight)
	#update
	sf.readline()
	throttle,brake = move(speed, distance, time,speedlimit,trafficLight)
	sf.write('throttle '+str(throttle)+'\n')
	sf.write('brake '+str(brake)+'\n')
	sf.flush()
