import polysim_pb2
import sys
import os
import numpy as np

nx = 2
ny = 2
l = 32
h = 2
if sys.argv[1]:
	fname = sys.argv[1]
else:
	fname = 'default'

outfile = open(fname,"wb")
sim = polysim_pb2.SSim()
#spread
sim.settings.h = .001
sim.settings.sk = 100
sim.settings.pk = 100
sim.settings.stiffk = 1
sim.settings.oseenk = .1
sim.settings.shiftk = .3
sim.settings.numpin = 1

sys = sim.system.add()



for i in range(nx):
    for j in range(ny):
        poly = sys.poly.add()
        current = np.array([1.1*i,1.1*j,h])
        for n in range(l):
            poly.x.append(current[0])
            poly.y.append(current[1])
            poly.z.append(current[2])
            
            for k in range(1000):#only try 1000 times, just in case
                temp = np.random.rand(3) - np.array([.5,.5,.2])
                temp = temp/np.linalg.norm(temp)
                if (temp[2] + current[2] > h):
                    break
            current = current + temp
            if current[2] < h:
                raise Exception

yolk = sim.yolk.add()
for i in range(3):
    part = np.random.rand(3)*5
    part[2] /= 2
    part[2] += .2
    yolk.x.append(part[0])
    yolk.y.append(part[1])
    yolk.z.append(part[2])

print(sim)
output = sim.SerializeToString()
outfile.write(output)
