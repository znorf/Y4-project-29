

# -*- coding: utf-8 -*-
"""
Created on Fri Mar 28 12:22:29 2025

@author: Max
"""

import numpy as np
import pandas as pd
df = pd.read_csv('nbox100.csv')
#df1 = pd.read_csv('P_pair_ids_100.csv')
data = pd.read_csv('100box.csv')
i = 0
P_id = []
while i < len(df):
    Pair_id= str(df.iloc[i,0])
    x=Pair_id.find(':')
    H0=int(Pair_id[:x])
    H1=int(Pair_id[x+1:])
    P_id.append(H0)
    P_id.append(H1)
    i+=1

Ppairs = []

i=0
j=0
while i < len(P_id):
    while j < len(data):
        if P_id[i] == data.iloc[j,5]:

            Ppairs.append(j)
            j=0
            break
        j+=1
    i+=1

#np.savetxt("Npairs1.csv", Ppairs, delimiter=",") #Physical takes about 10 mins to run! Non physical is 20 mins
