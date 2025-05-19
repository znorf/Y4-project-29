# -*- coding: utf-8 -*-
"""
Created on Thu May 15 18:10:26 2025

@author: Student
"""

# -*- coding: utf-8 -*-
"""
Created on Thu May 15 13:39:09 2025

@author: Student
"""

import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import numpy as np
from scipy.ndimage import gaussian_filter



#Sep
Nx_count = np.loadtxt("Nx_count_ds2.csv", delimiter=",")
Nx_count2 = np.loadtxt("Nx_count_ds2.csv", delimiter=",")

Px_count = np.loadtxt("Px_count_ds.csv", delimiter=",")
Px_count2 = np.loadtxt("Px_count_ds2.csv", delimiter=",")

Nx_val = np.loadtxt("Nx_val_ds2.csv", delimiter=",")
Nx_val2 = np.loadtxt("Nx_val_ds2.csv", delimiter=",")

Px_val = np.loadtxt("Px_val_ds.csv", delimiter=",")
Px_val2 = np.loadtxt("Px_val_ds2.csv", delimiter=",")

Nerrors_x = np.loadtxt("Nerrors_x_ds2.csv", delimiter=",")
Nerrors_x2 = np.loadtxt("Nerrors_x_ds2.csv", delimiter=",")

Perrors_x = np.loadtxt("Perrors_x_ds.csv", delimiter=",")
Perrors_x2 = np.loadtxt("Perrors_x_ds2.csv", delimiter=",")

Nerrors_y = np.loadtxt("Nerrors_y_ds2.csv", delimiter=",")
Nerrors_y2 = np.loadtxt("Nerrors_y_ds2.csv", delimiter=",")

Perrors_y = np.loadtxt("Perrors_y_ds.csv", delimiter=",")
Perrors_y2 = np.loadtxt("Perrors_y_ds2.csv", delimiter=",")

Pmidss_MR = np.loadtxt("Pmidss_ds2.csv", delimiter=",")
Nmidss_MR = np.loadtxt("Nmidss_ds2.csv", delimiter=",")
#errors_x2 = np.loadtxt("errors_x_MR (2).csv", delimiter=",")


MRlim1 = 2.75*10**13
MRlim2 = 3.7*10**13

MRlim3 = 4
MRlim4 = 5.2

excessER=((Nerrors_y*Nmidss_MR)**2+Perrors_y**2)**0.5
excess=Px_val/Px_count-Nx_val/Nx_count*Nmidss_MR
plt.figure()

fig= plt.figure()
ax=fig.gca()
fig.tight_layout(h_pad=0.01)

ax.errorbar(Nmidss_MR, Nx_val/Nx_count/10**14*Nmidss_MR, xerr=Nerrors_x, yerr=Nerrors_y*Nmidss_MR/10**14, fmt='.',color = 'blue', capsize=5, label='Non-physical')  #gives errors if divide by 0
ax.errorbar(Pmidss_MR, Px_val/Px_count/10**14, xerr=Perrors_x, yerr=Perrors_y/10**14, fmt='.',color = 'red', capsize=5, label='Physical')  #gives errors if divide by 0

ax.set_ylim(-0.2,6.5)
ax.set_xlim(3,20) 
ax.plot([-1,21],[0,0],linestyle='dashed')

ax.errorbar(Pmidss_MR, excess/10**14, xerr=Perrors_x, yerr=excessER/10**14, fmt='.',color = 'black', capsize=5, label='Excess')  #gives errors if divide by 0
ax.legend()


plt.xlabel('$ds$ ($Mpc$ $h^{-1}$)')
plt.ylabel('$M_{stack}$ ($10^{14}M_\odot h^{-1}$)')

#ax.set_xlim(0,1)
#ax.set_xlim(0,1)
ax.set_xticks(np.arange(3, 21, step=1))


plt.savefig('M-ds.pdf', dpi=1200,bbox_inches='tight')