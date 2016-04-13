import socket

maxvel = 14

def status(i):
    sock.send(bytes('STATUS %d\n' % i, 'UTF-8'))
    line = f.readline()
    return [float(el) for el in line.split()]

def throttle(i,val):
    sock.send(bytes('THROTTLE %d %f\n' % (i,val), 'UTF-8'))
    res = f.readline()

def tick(val):
    sock.send(bytes('TICK %f\n' % val, 'UTF-8'))
    res = f.readline()
    if 'SUCCESS' in res:
        return True
    return False

def solve(f):
    drones = int(f.readline())
    height = float(f.readline())
    print(drones,height)
    while True:
        for i in range(drones):
            x,y,z,vx,vy,vz,rx,ry,rz = status(i)
            print(x,y,z)
            if vz < 2:
                throttle(i,1.0)
            else:
                throttle(i,0.0)
        if tick(0.5):
            break

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost',7000))
f = sock.makefile()
solve(f)
f.close()
