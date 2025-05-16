# -*- coding: utf-8 -*-
"""
Created on Thu May 15 20:41:15 2025

@author: Student
"""

import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import numpy as np
from scipy.ndimage import gaussian_filter
import matplotlib.ticker as mticker


#Filament!
aP = np.loadtxt("PFilament.csv", delimiter=",")
aN = np.loadtxt("NFilament.csv", delimiter=",")
#aN = aN*2
comb = aP-aN

# Assuming pixel_array is your 2D or 3D array (for RGB images)
# For grayscale (2D array):
Psmoothed_array = gaussian_filter(aP, sigma=1.0)
Nsmoothed_array = gaussian_filter(aN, sigma=1.0)
PNsmoothed_array = gaussian_filter(comb, sigma=1.0)
PNNsmooth = Psmoothed_array-Nsmoothed_array
vmaxs = 148659184964
vmins = 17214854769
xedges = np.linspace(0, 100, 101)
X, Y = np.meshgrid((xedges[:-1] + xedges[1:]) / 2,
                   (xedges[:-1] + xedges[1:]) / 2)



#stacking
widths = 0.25

cmap = plt.colormaps["inferno"]

fig0=plt.figure()
ax0=fig0.gca()
#plt.title('Non-Physical pairs Smoothed')
im0=ax0.imshow(Nsmoothed_array,norm=LogNorm(vmin = vmins,vmax = vmaxs),cmap=cmap)
  
cb=fig0.colorbar(im0,pad=0,label='$\Sigma_{DM,H}$ ($10^{10}M_{\odot}Mpc^{-2}h$)',ticks=[2*10**10,3*10**10,4*10**10,6*10**10,8*10**10,10*10**10],format=mticker.FixedFormatter(['2', '', '4','6','8','10']))

#ax.axis('off')
ax0.set_xlim([0,100])
ax0.set_ylim([0,100])
ax0.set_xlabel('X (arb units)')
ax0.set_ylabel('Y (arb units)')
fig0.savefig('Non-Physical pairs Smoothed! no star.pdf', dpi=1200,bbox_inches='tight')
ax0.plot(np.array([25,75]),np.array([50,50]),color = 'red',marker='*',markersize=12)
fig0.savefig('Non-Physical pairs Smoothed!.pdf', dpi=1200,bbox_inches='tight')
ax0.contour(X, Y, Nsmoothed_array,linewidths=widths, colors='white')

fig0.savefig('Non-Physical pairs Smoothed!CONT.pdf', dpi=1200,bbox_inches='tight')


fig1=plt.figure()
ax1=fig1.gca()
#plt.title('Physical pairs Smoothed')
im1=ax1.imshow(Psmoothed_array,norm=LogNorm(vmin = vmins,vmax = vmaxs),cmap=cmap)
  
fig1.colorbar(im1,pad=0,ax=ax1,label='$\Sigma_{DM,H}$ ($10^{10}M_{\odot}Mpc^{-2}h$)',ticks=[2*10**10,3*10**10,4*10**10,6*10**10,8*10**10,10*10**10],format=mticker.FixedFormatter(['2', '', '4','6','8','10']))

#plt.axis('off')
ax1.set_xlim([0,100])
ax1.set_ylim([0,100])
ax1.set_xlabel('X (arb units)')
ax1.set_ylabel('Y (arb units)')
fig1.savefig('Physical pairs Smoothed! no star.pdf', dpi=1200,bbox_inches='tight')
ax1.plot(np.array([25,75]),np.array([50,50]),color = 'red',marker='*',markersize=12)
fig1.savefig('Physical pairs Smoothed!.pdf', dpi=1200,bbox_inches='tight')
ax1.contour(X, Y, Nsmoothed_array,linewidths=widths, colors='white')

fig1.savefig('Physical pairs Smoothed!CONT.pdf', dpi=1200,bbox_inches='tight')


fig2=plt.figure()
ax2=fig2.gca()
#plt.title('Filament Smoothed')
im2=ax2.imshow(PNsmoothed_array,vmin = -0.5*10**10,vmax = 74334841610,cmap=cmap)
  
fig2.colorbar(im2,pad=0,ax=ax2,label='$\Sigma_{DM,H}$ ($10^{10}M_{\odot}Mpc^{-2}h$)',ticks=[0*10**10,1*10**10,2*10**10,3*10**10,4*10**10,5*10**10,6*10**10,7*10**10], format=mticker.FixedFormatter(['0', '1', '2','3','4','5','6','7']))
#plt.axis('off')
ax2.set_xlim([0,100])
ax2.set_ylim([0,100])
ax2.set_xlabel('X (arb units)')
ax2.set_ylabel('Y (arb units)')


fig2.savefig('Filament Smoothed! Non log no star.pdf', dpi=1200,bbox_inches='tight')
ax2.plot(np.array([25,75]),np.array([50,50]),color = 'red',marker='*',markersize=12)
fig2.savefig('Filament Smoothed! Non log.pdf', dpi=1200,bbox_inches='tight')
ax2.contour(X, Y, Nsmoothed_array,linewidths=widths, colors='white')
fig2.savefig('Filament Smoothed! Non log CONT.pdf', dpi=1200,bbox_inches='tight')


