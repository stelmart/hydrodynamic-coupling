import polysim_pb2
from scipy import *
from pylab import *
import sys


#Import data from .sim
name = sys.argv[1]
file = open(sys.argv[1],"rb")
sim = polysim_pb2.SSim()
sim.ParseFromString(file.read())

ds = 0.2 #pixel size for density function
t_start = 4000
dt = 5 #number of frames per time step

pos_list = []
min_x = sys.maxint
max_x = -sys.maxint - 1

#Loop to find all x positions after t_start for every frame.
for (frame_num,sys) in enumerate(sim.system):
    scaled_time = frame_num-t_start
    if scaled_time>=0 & scaled_time%dt==0:
        for (poly_num,poly) in enumerate(sys.poly):
            x = int(poly.x[-1]/ds)
            pos_list.append([scaled_time/dt,x])
            if x > max_x:
                max_x = x
            if x < min_x:
                min_x = x            


nx = max_x - min_x + 1
nt = int(scaled_time/dt) + 1

#Round the above values up to the nearest 2^N

nx = int(2**(ceil(log2(nx))))
nt = int(2**(ceil(log2(nt))))

#Construct density function
dens = zeros((nt,nx))
for i in range(0, len(pos_list)):
    t = pos_list[i][0]
    x = pos_list[i][1] - min_x
    dens[t,x] += 1

#Zero-pad density function
dens = pad(dens, ((nt/2,nt/2),(nx/2,nx/2)),'constant')

print(nx)
print(nt)
 
#Find correlation function
ifft_dens = ifft2(dens)
ifft_dens[0,0] = 0
abs_ifft_dens = abs(ifft_dens)
ifft_dens_sq = abs_ifft_dens**2
fft_dens = fft2(ifft_dens_sq)
corr = real(fft_dens)

#Save into file for plotting later
savename =  name[:-4]+'_'+str(ds)
save(savename,corr)


    
