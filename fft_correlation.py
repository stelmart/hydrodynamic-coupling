import polysim_pb2
from scipy import *
from pylab import *
import sys


#Import data from .sim
name = sys.argv[1]
file = open(sys.argv[1],"rb")
sim = polysim_pb2.SSim()
sim.ParseFromString(file.read())

ds = 1.0 #pixel size for density function
t_start = 1500
dt = 25 #number of frames per time step

pos_list = []
min_x = sys.maxint
min_y = min_x
max_x = -sys.maxint - 1
max_y = max_x

#Loop to find all 2D positions after t_start for every frame.
for (frame_num,sys) in enumerate(sim.system):
    scaled_time = frame_num-t_start
    if scaled_time>=0 & scaled_time%dt==0:
        for (poly_num,poly) in enumerate(sys.poly):
            x = int(poly.x[-1]/ds)
            y = int(poly.y[-1]/ds)
            pos_list.append([scaled_time/dt,x,y])
            if x > max_x:
                max_x = x
            if y > max_y:
                max_y = y
            if x < min_x:
                min_x = x
            if y < min_y:
                min_y = y            


nx = max_x - min_x + 1
ny = max_y - min_y + 1
nt = int(scaled_time/dt) + 1

#Round the above values up to the nearest 2^N

nx = int(2**(ceil(log2(nx))))
ny = int(2**(ceil(log2(ny))))
nt = int(2**(ceil(log2(nt))))

#Construct density function
dens = zeros((nt,nx,ny))
for i in range(0, len(pos_list)):
    t = pos_list[i][0]
    x = pos_list[i][1] - min_x
    y = pos_list[i][2] - min_y
    dens[t,x,y] += 1


# Find average of density function and subtract
#dens_ave = sum(dens)/(dens.size)
#dens -= dens_ave

#Zero-pad density function
dens = pad(dens, ((nt/2,nt/2),(nx/2,nx/2),(ny/2,ny/2)),'constant')

print(nx)
print(ny)
print(nt)
 
#Find correlation function
ifft_dens = ifftn(dens)
ifft_dens[0,0,0] = 0
abs_ifft_dens = abs(ifft_dens)
ifft_dens_sq = abs_ifft_dens**2
fft_dens = fftn(ifft_dens_sq)
corr = real(fft_dens)

#Save into file for plotting later
savename =  name[:-4]+'_'+str(ds)
save(savename,corr)


    
