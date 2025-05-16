# -*- coding: utf-8 -*-
"""
Created on Thu May 15 16:45:20 2025

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



#MR
Nx_count = np.loadtxt("Nx_count_ds3.csv", delimiter=",")
Nx_count2 = np.loadtxt("Nx_count_ds4.csv", delimiter=",")

Px_count = np.loadtxt("Px_count_ds3.csv", delimiter=",")
Px_count2 = np.loadtxt("Px_count_ds4.csv", delimiter=",")

Nx_val = np.loadtxt("Nx_val_ds3.csv", delimiter=",")
Nx_val2 = np.loadtxt("Nx_val_ds4.csv", delimiter=",")

Px_val = np.loadtxt("Px_val_ds3.csv", delimiter=",")
Px_val2 = np.loadtxt("Px_val_ds4.csv", delimiter=",")

Nerrors_x = np.loadtxt("Nerrors_x_ds3.csv", delimiter=",")
Nerrors_x2 = np.loadtxt("Nerrors_x_ds4.csv", delimiter=",")

Perrors_x = np.loadtxt("Perrors_x_ds3.csv", delimiter=",")
Perrors_x2 = np.loadtxt("Perrors_x_ds4.csv", delimiter=",")

Nerrors_y = np.loadtxt("Nerrors_y_ds3.csv", delimiter=",")
Nerrors_y2 = np.loadtxt("Nerrors_y_ds4.csv", delimiter=",")

Perrors_y = np.loadtxt("Perrors_y_ds3.csv", delimiter=",")
Perrors_y2 = np.loadtxt("Perrors_y_ds4.csv", delimiter=",")

Pmidss_MR = np.loadtxt("Pmidss_ds3.csv", delimiter=",")
Nmidss_MR = np.loadtxt("Nmidss_ds3.csv", delimiter=",")
#errors_x2 = np.loadtxt("errors_x_MR (2).csv", delimiter=",")


MRlim1 = 2.75*10**13
MRlim2 = 3.7*10**13

MRlim3 = 4
MRlim4 = 5.2

excessER=(Nerrors_y2**2+Perrors_y2**2)**0.5
excess=Px_val2/Px_count2-Nx_val2/Nx_count2


fig, (ax1,ax2) = plt.subplots(2,1,sharex=True,gridspec_kw={'height_ratios': [2, 1]})
fig.tight_layout(h_pad=0.01)


ax1.errorbar(Nmidss_MR, Nx_val2/Nx_count2/10**13, xerr=Nerrors_x2, yerr=Nerrors_y2/10**13,color = 'red', fmt='.', capsize=5, label='Non-physical')  #gives errors if divide by 0
ax1.errorbar(Pmidss_MR, Px_val2/Px_count2/10**13, xerr=Perrors_x2, yerr=Perrors_y2/10**13, fmt='.',color = 'blue', capsize=5, label='Physical')
ax1.set_xlim([0,1])
ax1.set_xlim([2.7,3.7])


ax2.errorbar(Pmidss_MR, excess/10**13, xerr=Perrors_x, yerr=excessER/10**13, fmt='.',color = 'black', capsize=5, label='Excess')  #gives errors if divide by 0
ax2.set_ylim([0,0.5])
#ax2.set_yticks([0,.5])
ax2.set_xlim([0,1])
 

ax2.legend()
ax1.legend()

ax1.tick_params(
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom=False,      # ticks along the bottom edge are off
    top=False,         # ticks along the top edge are off
    labelbottom=False) # labels along the bottom edge are off
ax1.spines.bottom.set_visible(False)
ax2.spines.top.set_visible(False)
#ax1.xaxis.tick_top()
#ax1.tick_params(labeltop=False)  # don't put tick labels at the top
ax2.xaxis.tick_bottom()

d = .5  # proportion of vertical to horizontal extent of the slanted line
kwargs = dict(marker=[(-1, -d), (1, d)], markersize=12,
              linestyle="none", color='k', mec='k', mew=1, clip_on=False)
ax1.plot([0, 1], [0, 0], transform=ax1.transAxes, **kwargs)
ax2.plot([0, 1], [1, 1], transform=ax2.transAxes, **kwargs)


plt.xlabel('Mass Ratio (no units)')
plt.ylabel('$M_{stack}/ds$ ($10^{13}M_\odot h$ $Mpc^{-1}$)')
ax2.yaxis.set_label_coords(-0.075,1.3)

ax1.set_xlim(0,1)
ax2.set_xlim(0,1)


plt.savefig('M-ds-MR.pdf', dpi=1200,bbox_inches='tight')