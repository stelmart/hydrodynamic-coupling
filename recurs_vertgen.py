
from scipy import *
from pylab import *
from scipy import weave
from scipy.weave import converters
import polysim_pb2

import sys
import os
import numpy as np

def e_intersect_chains(r,chain_num,mon_num,cutoffsq):
   intersects=array([0])
   N,l,d = shape(r)
   code = """
   int i,j;
   for(i=0; i < N ; i++)
   {
      for(j=0; j < l;j++)
      {
	 int k;
	 double rsq=0;
	 for(k=0;k < 3; k++)
	 {
	    double diff = r(chain_num,mon_num,k)-r(i,j,k);
	    rsq += diff*diff;
	 }
	 if (rsq < cutoffsq && i != chain_num && j != mon_num)
	 {
	    intersects(0) += 1/rsq;
	 }
      }
   }
   """
   weave.inline(code, ['r', 'chain_num', 'mon_num', 'cutoffsq', 'N', 'l','intersects'], type_converters=converters.blitz, compiler = 'gcc', verbose=2)
   return intersects[0]


linksize=1.0
def springE(r,i,l):
   R = sqrt(sum((r[i,:]-r[i-1,:])**2))
   e = (R-linksize)**2
   if i < l-1:
      R = sqrt(sum((r[i,:]-r[i+1,:])**2))
      e += (R-linksize)**2
   return 0.5*sk*e

def ave_arclength(r):
   N,l,d = shape(r)
   arclength = 0.0
   for n in range(N):
      for i in range(1,l):
          arclength += sqrt(sum((r[n,i,:]-r[n,i-1,:])**2))
   return arclength/(N*(l-1))


def stiffE(r,i,l):
   e=0
   if i < l-2:
      e += sum((r[i+2,:]-r[i,:])**2)
   if i > 1:
      e += sum((r[i-2,:]-r[i,:])**2)
   return -stiffk*e


cutoff = 0.5
cutsq = cutoff**2
beta = 10.0

def system_intersect(r):
   count = 0
   N,l,d = shape(r)
   for n in range(N):
      for i in range(1,l):
           if e_intersect_chains(r,n,i,cutsq) > 0.0001:
	      count += 1
   return count

def wall_intersect(r):
   count = 0
   N,l,d = shape(r)
   for n in range(N):
      for i in range(1,l):
           if r[n,i,2] < h:
	      count += 1
   return count


def anneal_step(r):
   intersect_flag = 0
   wall_flag = 0
   N,l,d = shape(r)
   rold = zeros((d))
   step = 0.1
   half = np.array([.5,.5,.5])
   for n in range(N):
      for i in range(1,l):
           eold_int = e_intersect_chains(r,n,i,cutsq)
           temp = step*(np.random.rand(3) - half)
           dE = -(springE(r[n,:,:],i,l) + stiffE(r[n,:,:],i,l))
	   rold[:]  = r[n,i,:]
	   r[n,i,:] += temp[:]
	   if rold[2] < h:
	      wall_flag += 1

	   if r[n,i,2] < h:
	      r[n,i,:] = rold[:]
	      continue
           if e_intersect_chains(r,n,i,cutsq) > eold_int:
	      r[n,i,:] = rold[:]
	      intersect_flag += 1
	      continue
           dE += springE(r[n,:,:],i,l) + stiffE(r[n,:,:],i,l)
           if np.random.rand() > exp(-beta*dE):
  	       r[n,i,:]  = rold[:]

   return intersect_flag, wall_flag

def anneal(r):
    count = 0
    while (True):
       iflag, wflag = anneal_step(r)
       count += 1
       sys_int = system_intersect(r)
       print count,"num attempted chain inters: ", iflag," num wall xings: ", wflag, "num system inters: ",  sys_int, "ave arclength = ", ave_arclength(r)
       if wflag == 0 and sys_int == 0 and count > 300:
          return count

k_stiff = [0.3,0.4,0.5,0.6,0.7,0.8,0.9]
k_oseen = [0.01,0.02]

fdir = sys.argv[1]+'/'

for ii in range(len(k_stiff)):
    for jj in range(len(k_oseen)):
        nx = 128
        ny = 1
        l = 16
        h = 1.0
        spacing = 2

        sim = polysim_pb2.SSim()

        sim.settings.h = .0001
        sim.settings.sk = 100
        sk = sim.settings.sk
        sim.settings.pk = 100
        sim.settings.stiffk = k_stiff[ii]
        stiffk = sim.settings.stiffk
        sim.settings.oseenk = k_oseen[jj]
        sim.settings.shiftk = .2
        sim.settings.numpin = 1
        sim.settings.basek = 100 #basek is ALWAYS 100 regardless of what is entered here

        fname = fdir + 'ws-'+ str(sim.settings.oseenk) +'-'+str(sim.settings.stiffk)+'.sim'


        outfile = open(fname,"wb")


        sys = sim.system.add()



        N = nx*ny
        r = zeros((N,l,3))
        x_noise = 0.005

        for i in range(nx):
            for j in range(ny):
               for n in range(l):
                #current = np.array([2.*i,2.*j,h])
                  current = np.array([spacing*(i+x_noise*(1-2*random())),spacing*j,h*(n+1)])
	          pol_num = i*ny + j
                  r[pol_num,n,:] = current[:]
	        #for n in range(1,l):
                #   for k in range(1000):#only try 1000 times, just in case
                #        temp = np.random.rand(3) - np.array([.5,.5,.3])
                #        temp = temp/np.linalg.norm(temp)
                #        if (temp[2] + current[2] > h):
        	#	   break
        	#   current += temp
                #   r[pol_num,n,:] = current[:]

        #print "*****wall inter = ", wall_intersect(r)
        #anneal(r)

        for i in range(nx):
            for j in range(ny):
        	pol_num = i*ny + j
                poly = sys.poly.add()
                for n in range(l):
                    poly.x.append(r[pol_num,n,0])
                    poly.y.append(r[pol_num,n,1])
                    poly.z.append(r[pol_num,n,2])

                    if  r[pol_num,n,2] < h:
                        raise Exception

        yolk = sim.yolk.add()
        for i in range(1):
            part = np.random.rand(3)*20
            part[2] /= 2
            part[2] += .2
            yolk.x.append(part[0])
            yolk.y.append(part[1])
            yolk.z.append(part[2])

        print(sim)
        output = sim.SerializeToString()
        outfile.write(output)
