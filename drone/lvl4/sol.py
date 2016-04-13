import socket
import math

class Drone:
    def __init__(self,id,landpos):
        self.id = id
        self.pos = [0,0,0]
        self.speed = [0,0,0]
        self.orientation = [0,0,0]
        self.status = 'takeoff'
        self.starttime = -1
        self.topos = [0,0,30]
        self.landpos = landpos
        self.movetoheight = id*1+1

    def update(self):
        x,y,z,vx,vy,vz,rx,ry,rz = status(self.id)
        self.pos = [x,y,z]
        self.speed = [vx,vy,vz]
        self.orientation = [rx,ry,rz]

    def simulate(self, time):
        self.update()
        if self.status=='takeoff':
            if time==0:
                self.topos = self.pos[:]
                self.topos[2] = self.movetoheight
            if self.pos[2] > self.movetoheight-0.5:
                self.status = 'moveto'
                self.topos = self.landpos[:]
                self.topos[2] = self.movetoheight 
        if self.status=='moveto':
            if distance(self.pos,self.topos)<1:
                self.status = 'land'
                self.topos[2] = 0.29
        if self.status=='land':
            if self.pos[2]<0.3 and length(self.speed)<5 and abs(self.speed[2])<0.5:
                throttle(self.id,0.0)
                landres = land(self.id)
                if 'SUCCESS' in landres or 'OK' in landres:
                    return True
                return False


        tospeedx = min(4,max(-4,(self.topos[0]-self.pos[0])))
        tospeedy = min(4,max(-4,(self.topos[1]-self.pos[1])))
        tospeedz = min(2,max(-2,(self.topos[2]-self.pos[2])))
        deltaspeedx = tospeedx-self.speed[0]
        deltaspeedy = tospeedy-self.speed[1]
        deltaspeedz = tospeedz-self.speed[2]
        turn(self.id,[deltaspeedx,deltaspeedy,1])
        if deltaspeedz>0:
            throttle(self.id,min(deltaspeedz*2,1))
        else:
            throttle(self.id,0.0)
        return False

    def __str__(self):
        out = []
        out.append('status: ')
        out.append(self.status)
        out.append('Pos: ')
        out.append(str(self.pos))
        out.append('\nSpeed: ')
        out.append(str(self.speed))
        out.append('Orientation: ')
        out.append(str(self.orientation))
        out.append('\nLandpos: ')
        out.append(str(self.landpos))
        return ' '.join(out)

    def __repr__(self):
        return self.__str__()

def turn(i,arr):
    x,y,z = arr
    sock.send(bytes('TURN %d %f %f %f\n' % (i,x,y,z), 'UTF-8'))
    line = f.readline()

def distance(arr1,arr2):
    return length(el1-el2 for el1,el2 in zip(arr1,arr2))
def length(arr):
    return math.sqrt(sum(el*el for el in arr))

def status(i):
    sock.send(bytes('STATUS %d\n' % i, 'UTF-8'))
    line = f.readline()
    return [float(el) for el in line.split()]

def land(i):
    sock.send(bytes('LAND %d\n' % i, 'UTF-8'))
    res = f.readline()
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
    drones = int(f.readline())
    landpos = [[float(el) for el in f.readline().split()]+[0.0] for _ in range(drones)]
    drones = [Drone(i,pos) for i,pos in enumerate(landpos)]
    timeconstraint = float(f.readline())
    print(drones,timeconstraint)
    time = 0
    while len(drones)>0:
        time = tick(0)
        toremove = []
        for drone in drones:
            # print(drone)
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
