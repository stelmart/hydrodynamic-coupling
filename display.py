#!/usr/bin/python

from scipy import *
from pylab import *
import polysim_pb2
import time
import sys

print('Loading File...')

file = open(sys.argv[1],"rb")
sim = polysim_pb2.SSim()
sim.ParseFromString(file.read())
file.close()


print('Counting MTs...')

num_poly = 0
test = 1
for (frame_num,sys) in enumerate(sim.system):
	if test==1: 
		for (pol_num,poly) in enumerate(sys.poly):
			num_poly+=1
		test = 0

x = zeros((len(sim.system),num_poly))
y = zeros((len(sim.system),num_poly))

print('Storing end locations...')

for (frame_num,sys) in enumerate(sim.system):
	for (pol_num,poly) in enumerate(sys.poly):
		x[frame_num][pol_num] = poly.x[-1]
		y[frame_num][pol_num] = poly.y[-1]

print('Displaying...')

ion()
fig = figure(figsize=(12,0.25))
ax = fig.add_axes([0, 0, 1, 1], frameon=False)

frame_init = 3000
for frame_num in range(frame_init,len(sim.system)):
	if frame_num%100 == 0:
		print frame_num
        scat = ax.scatter(x[frame_num],y[frame_num],s=1)
        draw()
        pause(0.001)
        cla()
	
