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
	return speed, distance, time,speedlimit

def move(speed, distance, timetr,speedlimit):
	throttle = 100
	brake = 0
	if(speed*1.2>speedlimit[0] or (speed>speedlimit[2] and speedlimit[1]<100 and speedlimit[1]>0)):
		throttle = 0
		brake = 100
		
	if(distance>1500):
		throttle = 0
		brake = 100
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
