import socket
import math

class Drone:
    def __init__(self,id):
        self.id = id
        self.pos = [0,0,0]
        self.speed = [0,0,0]
        self.orientation = [0,0,0]
        self.status = 'takeoff'
        self.starttime = -1
        self.topos = [0,0,30]

    def update(self):
        x,y,z,vx,vy,vz,rx,ry,rz = status(self.id)
        self.pos = [x,y,z]
        self.speed = [vx,vy,vz]
        self.orientation = [rx,ry,rz]

    def simulate(self, time):
        self.update()
        if self.status=='takeoff' and self.pos[2]>20:
            if self.starttime<0:
                self.starttime = time
            if self.starttime+15<time:
                self.status = 'land'
                self.topos[2] = 0.29
        if self.status=='land':
            print(self.speed[2])
            if self.pos[2]<0.3 and length(self.speed)<5 and abs(self.speed[2])<0.5:
                throttle(self.id,0.0)
                landres = land(self.id)
                if 'SUCCESS' in landres or 'OK' in landres:
                    return True
                return False

        tospeed = min(2,max(-2,(self.topos[2]-self.pos[2])))
        deltaspeed = tospeed-self.speed[2]
        if deltaspeed>0:
            throttle(self.id,min(deltaspeed*2,1))
        else:
            throttle(self.id,0.0)
        return False

    def __str__(self):
        out = []
        out.append('Pos: ')
        out.append(str(self.pos))
        out.append('Speed: ')
        out.append(str(self.speed))
        out.append('Orientation: ')
        out.append(str(self.orientation))
        return ' '.join(out)

    def __repr__(self):
        return self.__str__()

def length(arr):
    return math.sqrt(sum(el*el for el in arr))

def status(i):
    sock.send(bytes('STATUS %d\n' % i, 'UTF-8'))
    line = f.readline()
    return [float(el) for el in line.split()]

def land(i):
    sock.send(bytes('LAND %d\n' % i, 'UTF-8'))
    res = f.readline()
    print(res)
    return res

def throttle(i,val):
    sock.send(bytes('THROTTLE %d %f\n' % (i,val), 'UTF-8'))
    res = f.readline()

def tick(val):
    sock.send(bytes('TICK %f\n' % val, 'UTF-8'))
    res = f.readline()
    if 'SUCCESS' in res:
        return True,0
    return float(res)

def solve(f):
    drones = [Drone(i) for i in range(int(f.readline()))]
    time = 0
    while len(drones)>0:
        time = tick(0)
        toremove = []
        for drone in drones:
            print(drone)
            if drone.simulate(time):
                toremove.append(drone)
        drones = [drone for drone in drones if drone not in toremove]
        if len(drones)==0:
            break
        if tick(0.05) is True:
            break

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost',7000))
f = sock.makefile()
solve(f)
f.close()
