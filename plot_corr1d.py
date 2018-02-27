from scipy import *
from numpy import *
import matplotlib.pyplot as plt
import sys

#load correlation function calculated with fft_correlation.py
name = sys.argv[1]
corr = load(sys.argv[1])


dims = shape(corr)

corr_norm = corr[0,0]
x_corr = corr[0,0:(dims[1]/2)]/corr_norm
t_corr = corr[0:dims[0]/2,0]/corr_norm

#set limits for graphs (as a fraction of maximum values of the functions)
x_lim = 1.0/2
t_lim = 1.0/2
y_lim = 1.1

#plot correlation functions
plt.figure(1)
plt.subplot(211)
plt.title('x correlation')
plt.ylim([y_lim*min(x_corr), y_lim*max(x_corr)])
plt.xlim([0, x_lim*len(x_corr)])
plt.plot(arange(len(x_corr)),x_corr)

plt.subplot(212)
plt.title('t correlation')
plt.ylim([y_lim*min(t_corr), y_lim*max(t_corr)])
plt.xlim([0, t_lim*len(t_corr)])
plt.plot(arange(len(t_corr)),t_corr)
plt.show()
