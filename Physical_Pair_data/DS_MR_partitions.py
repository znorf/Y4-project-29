# -*- coding: utf-8 -*-
"""
Created on Thu May  8 12:18:06 2025

@author: Student

"""

import pandas as pd
import numpy as np

N=8 #number of partitions

ds=pd.read_parquet('Physical_Pairs_ds.parquet')
ds=ds.values.tolist()

MR=pd.read_parquet('Physical_Pairs_massratio.parquet')
MR=MR.values.tolist()

for i in range(N):#creates the arrays
    globals()['ds'+str(i)]=[]
    globals()['MR'+str(i)]=[]


#creates the boundaries of partitions
dsR=np.linspace(3,20,N+1)
MRR=np.linspace(0,1,N+1)


#assigns each data point to it appropriate partition
for i in range(len(ds)):
    dsT=ds[i][0]
    MRT=MR[i][0]
    
    for j in range(N):
        if dsT>dsR[j] and dsT<=dsR[j+1]:
            globals()['ds'+str(j)].append(i)
        if j==0:
            if MRT>=MRR[j] and MRT<=MRR[j+1]:
                globals()['MR'+str(j)].append(i)
        else:
            if MRT>MRR[j] and MRT<=MRR[j+1]:
                globals()['MR'+str(j)].append(i)
    print(i)
            
