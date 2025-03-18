# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 11:30:06 2025

@author: Student
"""

import numpy as np
from sklearn.neighbors import NearestNeighbors
import pandas as pd

file = open('Rockstar_B.csv') #opens file containing the rockstar catalogue (above our minimum)
data = np.genfromtxt('Rockstar_B.csv', delimiter=',', dtype=str) #extracts data from file
file.close() #close file to minimise memory use

file = open('testdata.csv') #opens file containing the rockstar catalogue (above our minimum) and the repeated periodic points
testdata = np.genfromtxt('testdata.csv', delimiter=',', dtype=str) #extracts data from file
file.close() #close file to minimise memory use



r=20 #max radius of pairs

#grab coordinates and put them in a python list
x=testdata[1:,1:4]
x=x.astype('float64')

y=data[1:,1:4]
y=y.astype('float64')

samples=[]
haloes=[]
for i in range(0,len(x)):
    samples.append(x[i,0:4])

for i in range(0,len(y)):
    haloes.append(y[i,0:4])
  

#create headers for data set
p_pair_Id=['pair_ID_c']
p_pair_rock=['pair_ID_r']
p_pair_x0=['x0']
p_pair_x1=['x1']
p_pair_y0=['y0']
p_pair_y1=['y1']
p_pair_z0=['z0']
p_pair_z1=['z1']
p_pair_ds=['ds']
p_pair_m0=['m_vir_0']
p_pair_m1=['m_vir_1']
m0_m1=['mass_ratio']





neigh = NearestNeighbors(radius=r, metric='euclidean') #define conditions of nearest neighbour search

neigh.fit(samples) #create kd tree for samples
NearestNeighbors(radius=r)



#j-loop runs through all haloes (excluding non-contiguos)
for j in range(0,len(haloes)):
    
    #finds nearest neighbours 
    rng = neigh.radius_neighbors([haloes[j]],sort_results=True)
    dist=np.asarray(rng[0][0])
    pos=np.asarray(rng[1][0])
    
    #while loop removes all values below 3 mpc
    cond=True
    i=0
    while cond==True and i<len(pos):
        if dist[i]>3:
            dist=dist[i:]
            pos=pos[i:]
            cond=False
    
        i=i+1
    
    #for loop
    for i in range(0,len(dist)):
        if pos[i]>j:#condition ensures no duplication of pairs
            pair_id=str(j)+':'+str(pos[i])
            rock_id=str(data[j+1,4])+':'+str(testdata[pos[i]+1,4])
            p_pair_Id.append(pair_id)
            p_pair_rock.append(rock_id)
            
            p_pair_x0.append(float(data[j+1,1]))
            p_pair_x1.append(float(testdata[pos[i]+1,1]))
            
            p_pair_y0.append(float(data[j+1,2]))
            p_pair_y1.append(float(testdata[pos[i]+1,2]))
            
            p_pair_z0.append(float(data[j+1,3]))
            p_pair_z1.append(float(testdata[pos[i]+1,3]))
            
            m0=float(data[j+1,0])
            m1=float(testdata[pos[i]+1,0])
            
            p_pair_m0.append(m0)
            p_pair_m1.append(m1)
            if m0>m1:
                m0_m1.append(m1/m0)
            else:
                m0_m1.append(m0/m1)
            
            
        
            p_pair_ds.append("%.6g" %dist[i])
            
            
    print(j)


#create files, variables are deleted to minimise memory usage
del data,testdata, haloes, samples
p_pair_Id=np.array(p_pair_Id).reshape(-1, 1)
p_pair_rock=np.array(p_pair_rock).reshape(-1, 1)

arr=np.hstack((p_pair_Id,p_pair_rock))


df=pd.DataFrame(arr)
df.to_csv('Physical_Pairs_id.csv', index=False, header=False)

del p_pair_Id, p_pair_rock, df,arr



p_pair_x0=np.array(p_pair_x0).reshape(-1, 1)
p_pair_x1=np.array(p_pair_x1).reshape(-1, 1)

arr=np.hstack((p_pair_x0,p_pair_x1))

df=pd.DataFrame(arr)
df.to_csv('Physical_Pairs_x.csv', index=False, header=False)

del p_pair_x0, p_pair_x1, df,arr

p_pair_y0=np.array(p_pair_y0).reshape(-1, 1)
p_pair_y1=np.array(p_pair_y1).reshape(-1, 1)

arr=np.hstack((p_pair_y0,p_pair_y1))

df=pd.DataFrame(arr)
df.to_csv('Physical_Pairs_y.csv', index=False, header=False)

del p_pair_y0, p_pair_y1, df,arr

p_pair_z0=np.array(p_pair_z0).reshape(-1, 1)
p_pair_z1=np.array(p_pair_z1).reshape(-1, 1)

arr=np.hstack((p_pair_z0,p_pair_z1))

df=pd.DataFrame(arr)
df.to_csv('Physical_Pairs_z.csv', index=False, header=False)

del p_pair_z0, p_pair_z1, df,arr

p_pair_ds=np.array(p_pair_ds).reshape(-1, 1)
arr=p_pair_ds



df=pd.DataFrame(arr)
df.to_csv('Physical_Pairs_ds.csv', index=False, header=False)

del p_pair_ds, df,arr

p_pair_m0=np.array(p_pair_m0).reshape(-1, 1)
arr=p_pair_m0

df=pd.DataFrame(arr)
df.to_csv('Physical_Pairs_m0.csv', index=False, header=False)

del p_pair_m0, df,arr


p_pair_m1=np.array(p_pair_m1).reshape(-1, 1)
arr=p_pair_m1

df=pd.DataFrame(arr)
df.to_csv('Physical_Pairs_m1.csv', index=False, header=False)

del p_pair_m1, df,arr

m0_m1=np.array(m0_m1).reshape(-1, 1)
arr=m0_m1

df=pd.DataFrame(arr)
df.to_csv('Physical_Pairs_massratio.csv', index=False, header=False)

del m0_m1, df,arr