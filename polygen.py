import polysim_pb2
import sys
import os
import numpy as np

outfile = open(sys.argv[1],"wb")
if sys.argv[1] == "polygen.py":
	raise Exception()
sim = polysim_pb2.SSim()

sim.settings.h = .001
sim.settings.sk = 100
sim.settings.pk = 100
sim.settings.stiffk = 3
sim.settings.oseenk = .1
sim.settings.shiftk = .1
sim.settings.numpin = 1

sys = sim.system.add()



for i in range(20):
    for j in range(20):
        poly = sys.poly.add()
        current = np.array([2*i,2*j,.6])
        for n in range(64):
            poly.x.append(current[0])
            poly.y.append(current[1])
            poly.z.append(current[2])
            
            temp = np.random.rand(3) - np.array([.5,.5,0])
            temp = temp/np.linalg.norm(temp)
            current = current + temp

yolk = sim.yolk.add()
for i in range(10):
    part = np.random.rand(3)*20
    part[2] /= 2
    part[2] += .2
    yolk.x.append(part[0])
    yolk.y.append(part[1])
    yolk.z.append(part[2])

print(sim)
output = sim.SerializeToString()
outfile.write(output)
