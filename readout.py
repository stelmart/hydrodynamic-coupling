#!/usr/bin/python
import polysim_pb2
import sys
import os
file = open(sys.argv[1],"rb")
if sys.argv[1] == "jsonify.py":
	raise Exception()
sim = polysim_pb2.SSim()
sim.ParseFromString(file.read())
print("Settings")
print(sim.settings)
print("number of frames: ")
print(len(sim.system))
sum = 0
num = 0
for poly in sim.system[150].poly:
	for n in range(len(poly.x)-1):
		for poly2 in sim.system[150].poly:
			for m in range(len(poly2.x)-1):
				sum += (poly.x[n+1]-poly.x[n])*(poly.x[n+1]-poly.x[n])
				sum += (poly.y[n+1]-poly.y[n])*(poly.y[n+1]-poly.y[n])
				sum += (poly.z[n+1]-poly.z[n])*(poly.z[n+1]-poly.z[n])
				num += 1
print(sum/num)
