# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 17:36:38 2025

@author: Frederick de Naeyer
"""
import numpy as np 

file = open('top_10_rockstar.csv') #opens file containing top 10 highest mass haloes
data = np.genfromtxt('top_10_rockstar.csv', delimiter=',', dtype=str) #extracts data from file

pairs=np.array(['mvir_0','mvir_1','x0','y0','z0','x1','y1','z1']) #creates header of new data table
for i in range(1,10):
    for j in range(i+1,11):
        newrow=np.array([data[i,0],data[j,0],data[i,1],data[i,2],data[i,3],data[j,1],data[j,2],data[j,3]]) #creates new row of pair data
        pairs=np.vstack([pairs, newrow]) #adds new pair data to created array
