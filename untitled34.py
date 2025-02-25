# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 11:30:06 2025

@author: Student
"""

import numpy as np
from sklearn.neighbors import NearestNeighbors

file = open('Rockstar_A.csv') #opens file containing top 10 highest mass haloes
data = np.genfromtxt('Rockstar_A.csv', delimiter=',', dtype=str) #extracts data from file

n=len(data[:,0]) #number of data values

r=20


x=data[1:,1:4]
y=x[1:,0]
x=x.astype('float64')

samples=[]
for i in range(0,n-1):
    samples.append(x[i,0:4])



neigh = NearestNeighbors(radius=r)

neigh.fit(samples)
NearestNeighbors(radius=r)

rng = neigh.radius_neighbors([samples[0]])

print(np.asarray(rng[0][0]))
print((np.asarray(rng[1][0])))
l=len(np.asarray(rng[0][0]))
'''
for i in range(0,l):
    if (np.asarray(rng[0][0]))[i]<20:
        print((np.asarray(rng[0][0]))[i])
'''
