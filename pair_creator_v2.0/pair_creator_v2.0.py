# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 15:16:09 2025

@author: Student
"""

import numpy as np
import time

#start=time.time() #sets start time

file = open('top_1000_rockstar.csv') #opens file containing top 10 highest mass haloes
data = np.genfromtxt('top_1000_rockstar.csv', delimiter=',', dtype=str) #extracts data from file

n=len(data[:,0])-1 #number of data values


#for this example,physical pairs are stil stored in arrays.  this will be changed
p_Pairs=np.array(['mvir_0','mvir_1','x0','y0','z0','x1','y1','z1','ds','pair id']) #headers for physical pair table
np_Pairs='pair id' #pair_id column header

#creates connectivity array
conn=np.array(['id'])
conn=np.append(conn,data[1:,0])
conn_r=np.array(['connectivity'])
conn_r=np.append(conn_r,np.zeros([1000]))
conn=np.vstack([conn,conn_r]).T

#first set of for loops creates physical pairs
for i in range(1,n):
    for j in range(i+1,n+1):
        #calcaulates seperation, ds
        dx=float(data[i,1])-float(data[j,1])
        dy=float(data[i,2])-float(data[j,2])
        dz=float(data[i,3])-float(data[j,3])
        ds=np.sqrt(dx**2+dy**2+dz**2)
        if ds<=20 and ds>=3: #criteria for physical pairs
            
            pair_id=str(i)+';'+str(j) #pair id is combination of positions in list
            #adds physical pair to list
            newrow=np.array([data[i,0],data[j,0],data[i,1],data[i,2],data[i,3],data[j,1],data[j,2],data[j,3],ds,pair_id])
            p_Pairs=np.vstack([p_Pairs, newrow])
            #adds counts connections
            conn[i,1]=float(conn[i,1])+1
            conn[j,1]=float(conn[j,1])+1

#second set of for loops creates non-physical
for i in range(1,n):
    locals()['np_pairs_'+str(i)]='' #for each n interation, non-physical pairs are stored in seperate arrays
    for j in range(i+1,n+1):
        pair_id=str(i)+';'+str(j) #same as before
        if np.any(p_Pairs[:,9]==pair_id)==False: #checks whether pair is physical
            #calcaulates seperation, ds
            dx=float(data[i,1])-float(data[j,1])
            dy=float(data[i,2])-float(data[j,2])
            dz=float(data[i,3])-float(data[j,3])
            ds=np.sqrt(dx**2+dy**2+dz**2)
        if ds>20: #criteria for non-physical pairs
            locals()['np_pairs_'+str(i)]=locals()['np_pairs_'+str(i)]+','+pair_id #appends appropriate string
    #print(i) #print i after each n interation, just to eye-ball and debug programme
    
#for loop to combine seperate strings
for i in range(1,n):
    np_Pairs=np_Pairs+locals()['np_pairs_'+str(i)]
    del locals()['np_pairs_'+str(i)]

#tracks and prints run time
#end=time.time()
#print(end -start)
