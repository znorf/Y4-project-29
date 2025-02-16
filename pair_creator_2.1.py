# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 14:22:07 2025

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
p_Pairs_id ,np_Pairs_id='pair id','pair id' #pair_id column header
p_Pairs_m0 ,np_Pairs_m0='mvir_0','mvir_0'
p_Pairs_m1 ,np_Pairs_m1='mvir_1','mvir_1'

p_Pairs_x0 ,np_Pairs_x0='x_0','x_0'
p_Pairs_y0 ,np_Pairs_y0='y_0','y_0'
p_Pairs_z0 ,np_Pairs_z0='z_0','z_0'

p_Pairs_x1 ,np_Pairs_x1='x_1','x_1'
p_Pairs_y1 ,np_Pairs_y1='y_1','y_1'
p_Pairs_z1 ,np_Pairs_z1='z_1','z_1'

p_Pairs_ds ,np_Pairs_ds='ds','ds'
con=0




#first set of for loops creates physical pairs
for i in range(1,n):
    start=time.time()
    locals()['p_pairs_id'+str(i)]=''
    locals()['p_pairs_m0'+str(i)]=''
    locals()['p_pairs_m1'+str(i)]=''
    
    locals()['p_pairs_x0'+str(i)]=''
    locals()['p_pairs_y0'+str(i)]=''
    locals()['p_pairs_z0'+str(i)]=''
    
    locals()['p_pairs_x1'+str(i)]=''
    locals()['p_pairs_y1'+str(i)]=''
    locals()['p_pairs_z1'+str(i)]=''
    
    locals()['p_pairs_ds'+str(i)]=''
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
            
            locals()['p_pairs_id'+str(i)]=locals()['p_pairs_id'+str(i)]+','+pair_id
            
            locals()['p_pairs_m0'+str(i)]=locals()['p_pairs_m0'+str(i)]+','+str(data[i,0])
            
            locals()['p_pairs_m1'+str(i)]=locals()['p_pairs_m1'+str(i)]+','+data[j,0]
            
            locals()['p_pairs_x0'+str(i)]=locals()['p_pairs_x0'+str(i)]+','+data[i,1]
            
            locals()['p_pairs_y0'+str(i)]=locals()['p_pairs_y0'+str(i)]+','+data[i,2]
            
            locals()['p_pairs_z0'+str(i)]=locals()['p_pairs_z0'+str(i)]+','+data[i,3]
            
            locals()['p_pairs_x1'+str(i)]=locals()['p_pairs_x1'+str(i)]+','+data[j,1]
            locals()['p_pairs_y1'+str(i)]=locals()['p_pairs_y1'+str(i)]+','+data[j,2]
            locals()['p_pairs_z1'+str(i)]=locals()['p_pairs_z1'+str(i)]+','+data[j,3]
            locals()['p_pairs_ds'+str(i)]=locals()['p_pairs_ds'+str(i)]+','+str(ds)
                      
    t=time.time()-start
    print(i,t)
    

for i in range(1,n):
    p_Pairs_id=p_Pairs_id+locals()['p_pairs_id'+str(i)]

    p_Pairs_m0=p_Pairs_m0+locals()['p_pairs_m0'+str(i)]
    
    p_Pairs_m1=p_Pairs_m1+locals()['p_pairs_m1'+str(i)]
    
    p_Pairs_x0=p_Pairs_x0+locals()['p_pairs_x0'+str(i)]
    
    p_Pairs_y0=p_Pairs_y0+locals()['p_pairs_y0'+str(i)]
    
    p_Pairs_z0=p_Pairs_z0+locals()['p_pairs_z0'+str(i)]
    
    p_Pairs_x1=p_Pairs_x1+locals()['p_pairs_x1'+str(i)]
    
    p_Pairs_y1=p_Pairs_y1+locals()['p_pairs_y1'+str(i)]
    
    p_Pairs_z1=p_Pairs_z1+locals()['p_pairs_y1'+str(i)]
    
    p_Pairs_ds=p_Pairs_ds+locals()['p_pairs_ds'+str(i)]
    
    del locals()['p_pairs_id'+str(i)], locals()['p_pairs_m0'+str(i)], locals()['p_pairs_m1'+str(i)], locals()['p_pairs_x0'+str(i)], locals()['p_pairs_y0'+str(i)], locals()['p_pairs_z0'+str(i)], locals()['p_pairs_x1'+str(i)], locals()['p_pairs_y1'+str(i)], locals()['p_pairs_z1'+str(i)], locals()['p_pairs_ds'+str(i)]
    

result= np.array([list(map(str, p_Pairs_id.split(',')))]).T
np.savetxt('result.csv', result, delimiter=';',fmt='%s')
