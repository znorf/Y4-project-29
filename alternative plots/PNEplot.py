# -*- coding: utf-8 -*-
"""
Created on Thu May 15 13:09:58 2025

@author: Student
"""

import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import numpy as np
from scipy.ndimage import gaussian_filter

RN = np.loadtxt("NRad.csv", delimiter=",")
RP = np.loadtxt("PRad.csv", delimiter=",")

binss = np.arange(0.05,20,0.1)
midss = []
for i in range(len(binss) - 1):
    m =(((binss[i] + binss[i + 1])/2 ))
    midss.append(m)


select = 40046

# Assuming pixel_array is your 2D or 3D array (for RGB images)
# For grayscale (2D array):
RadMax = RP.max()/select
    
plt.figure()                                                               
plt.scatter(midss,RP/select/10**11,color = 'red',s=0.4)                                                              
plt.scatter(midss,RN/(select*2)/10**11,color = 'blue',s=0.4)
plt.scatter(midss,(RP/select-RN/(select*2))/10**11,color = 'black',s=0.4)
plt.plot([10**-2,10**2],[0,0],linestyle='dashed')

plt.xscale('log')
plt.xlim(0.1,20)
#plt.ylim(0,RadMax*1.1 )
#plt.title('Radius Mass Density')
plt.xlabel(r'R ($Mpc h^{-1}$)')
plt.ylabel(r'$\rho$ ($10^{11}$ $M_\odot$$Mpc^{-3}h^{-4}$)')


plt.legend(['Physical','Non-physical','Excess'])

plt.savefig('PNradius.pdf', dpi=1200,bbox_inches='tight')