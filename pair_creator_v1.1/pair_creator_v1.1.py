# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 14:09:48 2025

@author: Student
"""


import numpy as np


file = open('top_1000_rockstar.csv')
data = np.genfromtxt('top_1000_rockstar.csv', delimiter=',', dtype=str)

#n=len(data[:,0])-1
n=1000

p_Pairs=np.array(['mvir_0','mvir_1','x0','y0','z0','x1','y1','z1','ds'])
np_Pairs=np.array(['mvir_0','mvir_1','x0','y0','z0','x1','y1','z1','ds'])
#pairs=np.array(['id_0','id_1'])
conn=np.array(['id'])
conn=np.append(conn,data[1:,0])
conn_r=np.array(['connectivity'])
conn_r=np.append(conn_r,np.zeros([1000]))

conn=np.vstack([conn,conn_r]).T


"""
for i in range(1,n):
    print(i)
    for j in range(i+1,n+1):
        newrow=np.array([data[i,0],data[j,0],data[i,1],data[i,2],data[i,3],data[j,1],data[j,2],data[j,3]])
        pairs=np.vstack([pairs, newrow])
"""
#master_pair=np.array(['id_0','id_1'])
for i in range(1,n):
    print(i)
    for j in range(i+1,n+1):
        dx=float(data[i,1])-float(data[j,1])
        dy=float(data[i,2])-float(data[j,2])
        dz=float(data[i,3])-float(data[j,3])
        ds=np.sqrt(dx**2+dy**2+dz**2)
        if ds<=20 and ds>=3:
            """
            newrow=np.array([data[i,4],data[i,4]])
            pairs=np.vstack([pairs, newrow])
            """
            newrow=np.array([data[i,0],data[j,0],data[i,1],data[i,2],data[i,3],data[j,1],data[j,2],data[j,3],ds])
            p_Pairs=np.vstack([p_Pairs, newrow])
            conn[i,1]=float(conn[i,1])+1
            conn[j,1]=float(conn[j,1])+1
            

            
