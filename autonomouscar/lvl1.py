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
	return speed, distance, time

def move(speed, distance, timetr):
	throttle = 100
	brake = 0
	t.sleep(1)
	toDist = 500
	msSpeed = speed*KMH_TO_MS
	
	if(distance>500):
		throttle = 0
		brake = 100
	return throttle,brake

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 7000))
sf = s.makefile()
while(True):
	speed, distance, time = readData()
	print(speed, distance, time)
	#update
	sf.readline()
	throttle,brake = move(speed, distance, time)
	
	sf.write('throttle '+str(throttle)+'\n')
	sf.write('brake '+str(brake)+'\n')
	sf.flush()
