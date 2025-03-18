# -*- coding: utf-8 -*-
"""
Created on Tue Mar 18 12:46:30 2025

@author: Student
"""

import numpy as np
import matplotlib.pyplot as plt


fsize=10

xmin,xmax=2.5,20.5
ymin,ymax=-0.1,1.1

file = open('Physical_Pairs_ds.csv') #opens file containing the rockstar catalogue (above our minimum)
ds = np.genfromtxt('Physical_Pairs_ds.csv', delimiter=',', dtype=str) #extracts data from file
file.close() #close file to minimise memory use

file = open('Physical_Pairs_massratio.csv') #opens file containing the rockstar catalogue (above our minimum)
MR = np.genfromtxt('Physical_Pairs_massratio.csv', delimiter=',', dtype=str) #extracts data from file
file.close() #close file to minimise memory use

ds=ds[1:].astype('float64')
MR=MR[1:].astype('float64')

Z, xedges, yedges = np.histogram2d(ds, MR,bins=100,range=[[xmin, xmax], [ymin, ymax]])

fig = plt.figure()
ax = fig.gca()

ax.set_xlim([xmin, xmax])
ax.set_ylim([ymin, ymax])
plt.title( 'Mass Ratio vs Seperation distance for Physical pairs (extended)', fontsize=fsize)

cmap = plt.colormaps["inferno"]
jet = plt.pcolormesh(xedges, yedges, Z.T, cmap=cmap)


ax.set_xlabel( 'Seperation distance ($Mpc$ $h^{-1}$)', fontsize=fsize)
ax.set_ylabel( 'Mass ratio', fontsize=fsize)


fig.colorbar(jet, ax=ax, label="# points", pad=0)

fig.savefig( 'p_MRvsds_ex.jpg', dpi=300)


Z, xedges, yedges = np.histogram2d(ds, MR,bins=100,range=[[3, 20], [0, 1]])

fig1 = plt.figure()
ax1 = fig1.gca()

plt.title( 'Mass Ratio vs Seperation distance for Physical pairs', fontsize=fsize)

cmap = plt.colormaps["inferno"]
jet = plt.pcolormesh(xedges, yedges, Z.T, cmap=cmap)


ax1.set_xlabel( 'Seperation distance ($Mpc$ $h^{-1}$)', fontsize=fsize)
ax1.set_ylabel( 'Mass ratio', fontsize=fsize)


fig1.colorbar(jet, ax=ax1, label="# points", pad=0)

ax1.set_xlim([3, 20])
ax1.set_ylim([0, 1])
ax1.set_xticks(np.arange(3, 21, step=1))

fig.savefig( 'p_MRvsds.jpg', dpi=300)
