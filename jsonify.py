import polysim_pb2
import sys
import os
file = open(sys.argv[1],"rb")
if sys.argv[1] == "jsonify.py":
	raise Exception()
sim = polysim_pb2.SSim()
sim.ParseFromString(file.read())
output = open("out.json","w")
output.write("[")
for (n,sys) in enumerate(sim.system):
	output.write("[")
	for poly in sys.poly:
		output.write("[")
		for i in range(len(poly.x)):
			output.write("[" + ",".join((str(poly.x[i]),str(poly.y[i]),str(poly.z[i]))) + "]")
			output.write(",")
		output.seek(-1,os.SEEK_CUR)
		output.write("]")
		output.write(",")
	output.write("[")
	for i in range(len(sim.yolk[n].x)):
		output.write("[" + ",".join((str(sim.yolk[n].x[i]),str(sim.yolk[n].y[i]),str(sim.yolk[n].z[i]))) + "]")
		output.write(",")
	output.seek(-1,os.SEEK_CUR)
	output.write("]")
	output.write(",")  

	output.seek(-1,os.SEEK_CUR)
	output.write("]")
	output.write(",")
output.seek(-1,os.SEEK_CUR)
output.write("]")