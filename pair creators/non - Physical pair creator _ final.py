# -*- coding: utf-8 -*-
"""
Created on Fri Mar 14 16:45:40 2025

@author: Student
"""

from pandas import *
import numpy as np
from sklearn.neighbors import NearestNeighbors
import pandas as pd
import random

import time #optional, just to see how long things run for

file = open('Rockstar_B.csv') #opens file containing the rockstar catalogue (above our minimum mass)
data = np.genfromtxt('Rockstar_B.csv', delimiter=',', dtype=str) #extracts data from file
file.close() #close file to minimise memory use

def distance(a,b): #function calculates standard Euclidean distance
    dx2=(a[0]-b[0])**2
    dy2=(a[1]-b[1])**2
    dz2=(a[2]-b[2])**2
    
    ds=dx2+dy2+dz2
    ds=np.sqrt(ds)
    
    return ds

def npfind(position,distance,x,pc):#function finds non-physical pair id, separation distance, pair position in data
    
    
    cond=True
    while cond==True and len(position)!=0:
        y=random.randrange(0,len(position)) #random integer so pair creation is random
        target=position[y] #position of target is list of possible halo companions
        
        #if statment creates non-physical pair_id
        if target>int(pc):
            nid=pc+':'+str(target)
            first=int(pc)
            sec=target
        else:
            nid=str(target)+':'+pc
            sec=int(pc)
            first=target
            
        #checks if pair has already been created
        if sec in npairs[first]:  #or (str(target)==pc0 or str(target)==pc1) if excluding contiguous version of p-pair
            del position[y], distance[y]
        else:
            cond=False
    
    if len(position)==0:
        return 'no_pair' #if no pair found
    else:
        return nid, distance[y], position[y], first, sec

#grab coordinates and put them in a python list
y=data[1:,1:4]
y=y.astype('float64')

samples=[]
for i in range(0,len(y)):
    samples.append(y[i,0:4].tolist())


mass=data[1:,0] #array of mass values

npairs=[[] for _ in range(len(mass))] #empty list of lists to store non-physical pair ids

#creates array of mass values
starts=[]
masses=[] #array with bins of masses


for i in range(0,len(mass)):
    if mass[i-1] != mass[i]:
        starts.append(i)
        masses.append(float(mass[i]))
    #print(i) for debugging



datap=[] #masses and coords of haloes with that mass
pos=[] #positions of associated coords in our rockstar cat

for i in range(0,len(masses)):
    s=starts[i]
    if s==len(samples)-1:
        datap.append(samples[s:])
    else:
        e=starts[i+1]
        datap.append(samples[s:e])
        
    p=range(s,len(datap[i])+s)
    p=list(p)
    pos.append(p)
    print(i)


#grabs pair ids, both the our catalogue and the rockstar versions
data=read_csv('Physical_Pairs_id.csv')
p_ID_c=data['pair_ID_c'].tolist()
p_ID_r=data['pair_ID_r'].tolist()

#grabs rockstar id's of all haloes
data=read_csv('Rockstar_B.csv')
rockID=data['rockstarid'].tolist()


#grabs masses of haloes in physical pairs
data=read_csv('Physical_Pairs_m0.csv')
m0=data['m_vir_0'].tolist()
data=read_csv('Physical_Pairs_m1.csv')
m1=data['m_vir_1'].tolist()

del data

pid=['physical_pair_id'] #physical pair id
aid=['a_physical_pair_id'] #physical pair id, with non-contiguous haloes de-transformed


n0=['np_id_0'] #non-physical pair id for pair with halo 0
n1=['np_id_1'] #non-physical pair id for pair with halo 1

#coords of haloes in physical pair
Hp0=[['Hp0_x','y','z']] 
Hp1=[['Hp1_x','y','z']]

#coords of non-physical pair halo counterparts
Hn0=[['Hn0_x','y','z']]
Hn1=[['Hn1_x','y','z']]

#seperation distances of non-physical pairs
Ds0=['ds0']
Ds1=['ds1']


no=[['no_pairs_pos','P0','P1']] #list of pairs with no possible non-physical pairs



L=len(p_ID_c)

t0=time.time()
for j in range(0,L):      #len(p_ID_c)
    
    #physical pair ids
    pairc=p_ID_c[j]
    pairr=p_ID_r[j]
    
    #grabs coordinate data for haloes of matching masses
    x0=masses.index(m0[j])
    x1=masses.index(m1[j])
    C0=datap[x0]
    C1=datap[x1]
    
        
    #creates physical pair id, with non-contiguous haloes de-transformed
    x=pairc.find(':')
    pid.append(pairc)
    pc0=pairc[:x]
    if not('+' in pairr or '-' in pairr):#condtion for non-contiguos pairs
        aid.append(pairc)
        pc1=pairc[x+1:]
    else:
        pr1=int(pairr[len(pairr)-11:])
        i = rockID.index(pr1) if pr1 in rockID else None
        pc1=str(i)
        aid.append(pc0+':'+pc1)
    
    #grabs coords of physical pairs
    H0=samples[int(pc0)]
    H1=samples[int(pc1)]    
    Hp0.append(H0)
    Hp1.append(H1)
    
    D0=[] #distances to halo 0
    #positions in data
    P0=[]
    bigP=pos[x1]
    for i in range(0,len(C1)):
        dist=distance(H0, C1[i]) #calculates distances
        if dist>20: #appends if releveant halo
            D0.append(dist)
            P0.append(bigP[i])
            
    D1=[] #distances to halo 1
    #positions in data
    P1=[]
    bigP=pos[x0]
    for i in range(0,len(C0)):
        dist=distance(H1, C0[i]) #calculates distances
        if dist>20: #appends if relevant halo
            D1.append(dist)
            P1.append(bigP[i])
    
    
    find0=npfind(P0, D0, x1, pc0) #finds pair for halo 0
    find1=npfind(P1, D1, x0, pc1) #finds pair for halo 1
    
    
    #appends relevant data
    if find0=='no_pair':
        n0.append('no_pair')
        Hn0.append([-1,-1,-1])
        Ds0.append(-1.0)
        
    else:
        n0.append(find0[0])
        Ds0.append(find0[1])
        position=find0[2]
        Hn0.append(samples[position])
        f,s=find0[3:]
        npairs[f].append(s)
        #del position
    
    
    #del D0, P0, find0
    
    if find1=='no_pair':
        n1.append('no_pair')
        Hn1.append([-1,-1,-1])
        Ds1.append(-1.0)

    else:
        n1.append(find1[0])
        Ds1.append(find1[1])
        position=find1[2]
        Hn1.append(samples[position])
        
        f,s=find1[3:]
        npairs[f].append(s)
        
        #del position
        
    #del D1, P1, find1
    
    #stores positions of no_pair data
    if find0=='no_pair' and find1=='no_pair':
        no.append([j,1,1])
    elif find0=='no_pair':
        no.append([j,1,0])
    elif find1=='no_pair':
        no.append([j,0,1])
    
    
    #to check progress
    if j%10==0:
        print((j+1)/L)
    
      
t0=time.time()-t0

print(t0) # prints time taken

#for debugging
#j=(j+1)/len(p_ID_c)

#print(t0/j)



#save data to files

npairs=np.asarray(npairs, dtype = object)

df=pd.DataFrame(npairs)
df.to_csv('n_Physical_Pairs.csv', index=False, header=False)

del npairs


pid=np.array(pid).reshape(-1, 1)

df=pd.DataFrame(pid)
df.to_csv('n_Physical_Pairs_pid.csv', index=False, header=False)

del pid

aid=np.array(aid).reshape(-1, 1)

df=pd.DataFrame(aid)
df.to_csv('n_Physical_Pairs_aid.csv', index=False, header=False)

del aid

n0=np.array(n0).reshape(-1, 1)

df=pd.DataFrame(n0)
df.to_csv('n_Physical_Pairs_n0.csv', index=False, header=False)

del n0

n1=np.array(n1).reshape(-1, 1)

df=pd.DataFrame(n1)
df.to_csv('n_Physical_Pairs_n1.csv', index=False, header=False)

del n1

Hp0=np.array(Hp0).reshape(-1, 3)

df=pd.DataFrame(Hp0)
df.to_csv('n_Physical_Pairs_Hp0.csv', index=False, header=False)

del Hp0


Hp1=np.array(Hp1).reshape(-1, 3)

df=pd.DataFrame(Hp1)
df.to_csv('n_Physical_Pairs_Hp1.csv', index=False, header=False)

del Hp1

Hn0=np.array(Hn0).reshape(-1, 3)

df=pd.DataFrame(Hn0)
df.to_csv('n_Physical_Pairs_Hn0.csv', index=False, header=False)

del Hn0


Hn1=np.array(Hn1).reshape(-1, 3)

df=pd.DataFrame(Hn1)
df.to_csv('n_Physical_Pairs_Hn1.csv', index=False, header=False)

del Hn1

Ds0=np.array(Ds0).reshape(-1, 1)

df=pd.DataFrame(Ds0)
df.to_csv('n_Physical_Pairs_Ds0.csv', index=False, header=False)

del Ds0

Ds1=np.array(Ds1).reshape(-1, 1)

df=pd.DataFrame(Ds1)
df.to_csv('n_Physical_Pairs_Ds1.csv', index=False, header=False)

del Ds1

no=np.array(no).reshape(-1, 3)

df=pd.DataFrame(no)
df.to_csv('n_Physical_Pairs_no.csv', index=False, header=False)

del no