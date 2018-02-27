from scipy import *
from numpy import *
import matplotlib.pyplot as plt
import sys

#load correlation function calculated with fft_correlation.py
name = sys.argv[1]
corr = load(sys.argv[1])


dims = shape(corr)

corr_norm = corr[0,0,0]
x_corr = corr[0,0:(dims[1]/2),0]/corr_norm
y_corr = corr[0,0,0:(dims[2]/2)]/corr_norm
t_corr = corr[0:dims[0]/2,0,0]/corr_norm

#calculate the radial correlation function
nr = max(dims[1],dims[2])/2
r_corr = zeros(nr)
r_count = zeros(nr)
for i in range(0, dims[1]/2):
    for j in range(0, dims[2]/2):
        r = int(sqrt(i**2 + j**2))
        if r<nr:
            r_corr[r] += corr[0,i,j]
            r_count[r] += 1

#Average over number of bins per radius
for i in range(0,nr):
    r_corr[i] /= r_count[i]

r_corr /= r_corr[0]

#set limits for graphs (as a fraction of maximum values of the functions)
y_lim = 1.1
x_lim = 1.0

#plot correlation functions
plt.figure(1)
plt.subplot(221)
plt.title('x correlation')
plt.ylim([y_lim*min(x_corr), y_lim*max(x_corr)])
plt.xlim([0, x_lim*len(x_corr)])
plt.plot(arange(len(x_corr)),x_corr)

plt.subplot(222)
plt.title('y correlation')
plt.ylim([y_lim*min(y_corr), y_lim*max(y_corr)])
plt.xlim([0, x_lim*len(y_corr)])
plt.plot(arange(len(y_corr)),y_corr)

plt.subplot(223)
plt.title('r correlation')
plt.ylim([y_lim*min(r_corr), y_lim*max(r_corr)])
plt.xlim([0, x_lim*len(r_corr)])
plt.plot(arange(len(r_corr)),r_corr)

plt.subplot(224)
plt.title('t correlation')
plt.ylim([y_lim*min(t_corr), y_lim*max(t_corr)])
plt.xlim([0, x_lim*len(t_corr)])
plt.plot(arange(len(t_corr)),t_corr)
plt.show()
