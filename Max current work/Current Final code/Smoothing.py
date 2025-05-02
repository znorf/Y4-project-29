# -*- coding: utf-8 -*-

import numpy as np

import matplotlib.pyplot as plt

from matplotlib.colors import LogNorm


# Read the image

aP = np.loadtxt("PFilament.csv", delimiter=",")

aN = np.loadtxt("NFilament.csv", delimiter=",")
aN = aN/2
comb = aP-aN
'''
plt.figure()
plt.imshow(aP,norm=LogNorm())                                                         #Plot the mass density histogram
plt.colorbar()
plt.plot(np.array([25,75]),np.array([50,50]),color = 'red',marker='*',markersize=12)        #Red stars to show the location of the physical pair clusters
plt.axis('scaled')
plt.savefig('Phy1.png')  # Saves as PNG

plt.figure()
plt.imshow(aN)                                                         #Plot the mass density histogram
plt.colorbar()
plt.plot(np.array([25,75]),np.array([50,50]),color = 'red',marker='*',markersize=12)        #Red stars to show the location of the physical pair clusters
plt.axis('scaled')
plt.savefig('Non1.png')  # Saves as PNG
'
plt.figure()
plt.imshow(comb)                                                         #Plot the mass density histogram
plt.colorbar()
plt.imshow(aN,norm=LogNorm())
plt.plot(np.array([25,75]),np.array([50,50]),color = 'red',marker='*',markersize=12)        #Red stars to show the location of the physical pair clusters
plt.axis('scaled')
plt.savefig('combinedLog1.png')  # Saves as PNG
#image = cv2.imread('input.jpg')

# 1. Gaussian Blur
#gaussian_blur = cv2.GaussianBlur(image, (5, 5), 0)  # (5,5) is kernel size, 0 is sigmaX
'''
import numpy as np
from scipy.ndimage import gaussian_filter

# Assuming pixel_array is your 2D or 3D array (for RGB images)
# For grayscale (2D array):
Nsmoothed_array = gaussian_filter(aN, sigma=3.0)
plt.figure()
plt.title('Non-Physical pairs Smoothed')
plt.imshow(Nsmoothed_array,norm=LogNorm())
plt.plot(np.array([25,75]),np.array([50,50]),color = 'red',marker='*',markersize=12)  
plt.colorbar()
plt.figure()
plt.title('Non-Physical pairs')
plt.imshow(aN,norm=LogNorm())
plt.colorbar()
plt.plot(np.array([25,75]),np.array([50,50]),color = 'red',marker='*',markersize=12)  
Psmoothed_array = gaussian_filter(aP, sigma=3.0)
plt.figure()
plt.title('Physical pairs Smoothed')
plt.imshow(Psmoothed_array,norm=LogNorm())
plt.plot(np.array([25,75]),np.array([50,50]),color = 'red',marker='*',markersize=12)  
plt.colorbar()
plt.figure()
plt.title('Physical pairs ')
plt.imshow(aP,norm=LogNorm())
plt.colorbar()
plt.plot(np.array([25,75]),np.array([50,50]),color = 'red',marker='*',markersize=12)  
PNsmoothed_array = gaussian_filter(comb, sigma=3.0)
plt.figure()
plt.title('Filament Smoothed')
plt.imshow(PNsmoothed_array,norm=LogNorm())
plt.plot(np.array([25,75]),np.array([50,50]),color = 'red',marker='*',markersize=12)  
plt.colorbar()
plt.figure()
plt.title('Filament')
plt.imshow(comb,norm=LogNorm())
plt.colorbar()
plt.plot(np.array([25,75]),np.array([50,50]),color = 'red',marker='*',markersize=12)  
