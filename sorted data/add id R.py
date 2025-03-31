# -*- coding: utf-8 -*-
"""
Created on Mon Mar 31 18:48:38 2025

@author: Student
"""

import numpy as np
from pandas import *
import pandas as pd

file = open('Rockstar_B_100.csv') #opens file containing the rockstar catalogue (above our minimum)
data = np.genfromtxt('Rockstar_B_100.csv', delimiter=',', dtype=str)[1:,4] #extracts data from file
file.close() #close file to minimise memory use

file = open('n_Physical_Pairs_aid_100.csv') #opens file containing the rockstar catalogue (above our minimum)
idp = np.genfromtxt('n_Physical_Pairs_aid_100.csv', delimiter=',', dtype=str)[1:] #extracts data from file
file.close() #close file to minimise memory use

file = open('n_Physical_Pairs_n0_100.csv') #opens file containing the rockstar catalogue (above our minimum)
n0 = np.genfromtxt('n_Physical_Pairs_n0_100.csv', delimiter=',', dtype=str)[1:] #extracts data from file
file.close() #close file to minimise memory use

file = open('n_Physical_Pairs_n1_100.csv') #opens file containing the rockstar catalogue (above our minimum)
n1 = np.genfromtxt('n_Physical_Pairs_n1_100.csv', delimiter=',', dtype=str)[1:] #extracts data from file
file.close() #close file to minimise memory use

idpr=['aid_r']
n0r=['n0_r']
n1r=['n1_r']

for i in range(len(n0)):
    p=idp[i].split(':')
    n0T=n0[i].split(':')
    n1T=n1[i].split(':')
    
    p[0],p[1]=data[int(p[0])],data[int(p[1])]
    
    n0T[0],n0T[1]=data[int(n0T[0])],data[int(n0T[1])]
    
    n1T[0],n1T[1]=data[int(n1T[0])],data[int(n1T[1])]
    
    p=':'.join(p)
    n0T=':'.join(n0T)
    n1T=':'.join(n1T)
    
    idpr.append(p)
    n0r.append(n0T)
    n1r.append(n1T)
    
    
df=DataFrame(idpr)
df.to_csv('n_Physical_Pairs_aid_R_100.csv', index=False, header=False)

df=DataFrame(n0r)
df.to_csv('n_Physical_Pairs_n0_R_100.csv', index=False, header=False)

df=DataFrame(n1r)
df.to_csv('n_Physical_Pairs_n1_R_100.csv', index=False, header=False)

