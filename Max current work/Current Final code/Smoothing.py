# -*- coding: utf-8 -*-

import numpy as np

import matplotlib.pyplot as plt

from matplotlib.colors import LogNorm


# Read the image

aP = np.loadtxt("PFilament.csv", delimiter=",")

aN = np.loadtxt("NFilament.csv", delimiter=",")
#aN = aN/2
comb = aP-aN

plt.figure()
plt.imshow(aP,norm=LogNorm())                                                         #Plot the mass density histogram
plt.colorbar()
plt.plot(np.array([25,75]),np.array([50,50]),color = 'red',marker='*',markersize=12)        #Red stars to show the location of the physical pair clusters
plt.axis('scaled')
plt.savefig('Phy2.png')  # Saves as PNG

plt.figure()
plt.imshow(aN)                                                         #Plot the mass density histogram
plt.colorbar()
plt.plot(np.array([25,75]),np.array([50,50]),color = 'red',marker='*',markersize=12)        #Red stars to show the location of the physical pair clusters
plt.axis('scaled')
plt.savefig('Non2.png')  # Saves as PNG

plt.figure()
plt.imshow(comb)                                                         #Plot the mass density histogram
plt.colorbar()
plt.imshow(aN,norm=LogNorm())
plt.plot(np.array([25,75]),np.array([50,50]),color = 'red',marker='*',markersize=12)        #Red stars to show the location of the physical pair clusters
plt.axis('scaled')

#image = cv2.imread('input.jpg')

# 1. Gaussian Blur
#gaussian_blur = cv2.GaussianBlur(image, (5, 5), 0)  # (5,5) is kernel size, 0 is sigmaX

import numpy as np
from scipy.ndimage import gaussian_filter

# Assuming pixel_array is your 2D or 3D array (for RGB images)
# For grayscale (2D array):
Psmoothed_array = gaussian_filter(aP, sigma=3.0)
Nsmoothed_array = gaussian_filter(aN, sigma=3.0)
PNsmoothed_array = gaussian_filter(comb, sigma=3)
PNNsmooth = Psmoothed_array-Nsmoothed_array

plt.figure()
plt.title('Filament Smoothed')
plt.imshow(PNNsmooth,norm=LogNorm())
plt.plot(np.array([25,75]),np.array([50,50]),color = 'red',marker='*',markersize=12)  
plt.colorbar()
plt.savefig('Non-Physical pairs Smoothed2.png')


plt.figure()
plt.title('Filament Smoothed')
plt.imshow(PNNsmooth*-1,norm=LogNorm())
plt.plot(np.array([25,75]),np.array([50,50]),color = 'red',marker='*',markersize=12)  
plt.colorbar()
plt.savefig('Non-Physical pairs Smoothed2.png')

plt.figure()
plt.title('Non-Physical pairs Smoothed')
plt.imshow(Nsmoothed_array,norm=LogNorm())
plt.plot(np.array([25,75]),np.array([50,50]),color = 'red',marker='*',markersize=12)  
plt.colorbar()
plt.savefig('Non-Physical pairs Smoothed2.png')
plt.figure()
plt.title('Non-Physical pairs')
plt.imshow(aN,norm=LogNorm())
plt.colorbar()
plt.plot(np.array([25,75]),np.array([50,50]),color = 'red',marker='*',markersize=12)  

plt.savefig('Non-Physical pairs2')

plt.figure()
plt.title('Physical pairs Smoothed')
plt.imshow(Psmoothed_array,norm=LogNorm())
plt.plot(np.array([25,75]),np.array([50,50]),color = 'red',marker='*',markersize=12)  
plt.colorbar()
plt.savefig('Physical pairs Smoothed2.png')

plt.figure()
plt.title('Physical pairs')
plt.imshow(aP,norm=LogNorm())
plt.colorbar()
plt.plot(np.array([25,75]),np.array([50,50]),color = 'red',marker='*',markersize=12)  


plt.savefig('Physical pairs2.png')

plt.figure()
plt.title('Filament Smoothed')
plt.imshow(PNsmoothed_array)
plt.plot(np.array([25,75]),np.array([50,50]),color = 'red',marker='*',markersize=12)  
plt.colorbar()
plt.savefig('Filament Smoothed2.png')

plt.figure()
plt.title('Filament Smoothed')
plt.imshow(PNsmoothed_array,norm=LogNorm())
plt.plot(np.array([25,75]),np.array([50,50]),color = 'red',marker='*',markersize=12)  
plt.colorbar()
plt.savefig('Filament Smoothed.png')

PNNewSmooth = (Psmoothed_array - Nsmoothed_array)*-1
plt.figure()
plt.title('Filament Smoothed')
plt.imshow(PNNewSmooth,norm=LogNorm())
plt.plot(np.array([25,75]),np.array([50,50]),color = 'red',marker='*',markersize=12)  
plt.colorbar()
plt.savefig('Filament Smoothed2.png')
